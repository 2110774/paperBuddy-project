from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Application, Student, Scholarship, User, Notification
from datetime import datetime

applications_bp = Blueprint('applications', __name__)


@applications_bp.route('/', methods=['GET'])
@jwt_required()
def list_applications():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if user.role == 'student':
        student = user.student_profile
        if not student:
            return jsonify({'applications': []}), 200
        apps = Application.query.filter_by(student_id=student.id).all()
    elif user.role in ['admin', 'school']:
        apps = Application.query.all()
    else:
        return jsonify({'error': 'Unauthorized'}), 403

    result = []
    for app in apps:
        d = app.to_dict()
        if app.scholarship:
            d['scholarship_name'] = app.scholarship.name
            d['scholarship_type'] = app.scholarship.type
            d['scholarship_amount'] = app.scholarship.amount
            d['deadline'] = app.scholarship.deadline.isoformat() if app.scholarship.deadline else None
        result.append(d)

    return jsonify({'applications': result}), 200


@applications_bp.route('/', methods=['POST'])
@jwt_required()
def create_application():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if user.role != 'student' or not user.student_profile:
        return jsonify({'error': 'Only students can apply'}), 403

    data = request.get_json()
    scholarship_id = data.get('scholarship_id')
    if not scholarship_id:
        return jsonify({'error': 'scholarship_id required'}), 400

    scholarship = Scholarship.query.get_or_404(scholarship_id)
    student = user.student_profile

    # Check for duplicate
    existing = Application.query.filter_by(
        student_id=student.id,
        scholarship_id=scholarship_id
    ).first()
    if existing:
        return jsonify({'error': 'Already applied to this scholarship'}), 409

    # Calculate fit score
    from app.ai.recommendation import calculate_fit_score
    student_data = {
        'annual_income': student.annual_income or 0,
        'cgpa': student.cgpa or 0,
        'percentage': student.percentage or 0,
        'state': student.state or '',
        'category': student.category or '',
        'gender': student.gender or '',
        'degree': student.degree or '',
        'disability_status': student.disability_status,
    }
    fit_result = calculate_fit_score(student_data, scholarship.to_dict())

    app = Application(
        student_id=student.id,
        scholarship_id=scholarship_id,
        status='submitted',
        fit_score=fit_result['score'],
        selection_probability=fit_result['probability'],
        essay=data.get('essay', ''),
        submitted_at=datetime.utcnow(),
    )
    db.session.add(app)

    # Add notification
    notif = Notification(
        user_id=user_id,
        title='Application Submitted',
        message=f'Your application for {scholarship.name} has been submitted successfully.',
        type='application',
    )
    db.session.add(notif)
    db.session.commit()

    return jsonify({'message': 'Application submitted', 'application': app.to_dict()}), 201


@applications_bp.route('/<int:app_id>', methods=['GET'])
@jwt_required()
def get_application(app_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    app = Application.query.get_or_404(app_id)

    if user.role == 'student' and (not user.student_profile or app.student_id != user.student_profile.id):
        return jsonify({'error': 'Unauthorized'}), 403

    d = app.to_dict()
    if app.scholarship:
        d['scholarship'] = app.scholarship.to_dict()
    return jsonify(d), 200


@applications_bp.route('/<int:app_id>/status', methods=['PUT'])
@jwt_required()
def update_status(app_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if user.role not in ['admin', 'school']:
        return jsonify({'error': 'Unauthorized'}), 403

    app = Application.query.get_or_404(app_id)
    data = request.get_json()
    status = data.get('status')

    valid_statuses = ['draft', 'submitted', 'under_review', 'approved', 'rejected', 'disbursed']
    if status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400

    app.status = status
    app.reviewer_notes = data.get('notes', '')
    if status in ['approved', 'rejected']:
        app.reviewed_at = datetime.utcnow()
    if status == 'approved':
        app.amount_approved = data.get('amount_approved', app.scholarship.amount if app.scholarship else 0)

    # Send notification to student
    student_user = User.query.get(app.student.user_id)
    if student_user:
        msg = f'Your application for {app.scholarship.name if app.scholarship else "scholarship"} has been {status}.'
        notif = Notification(
            user_id=student_user.id,
            title=f'Application {status.capitalize()}',
            message=msg,
            type='application',
        )
        db.session.add(notif)

    db.session.commit()
    return jsonify({'message': 'Status updated', 'application': app.to_dict()}), 200
