from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Student, User, Application, Scholarship, Notification
from app.ai.recommendation import recommend_scholarships
from app.ai.financial_health import calculate_financial_health
from app.ai.dropout import predict_dropout_risk

students_bp = Blueprint('students', __name__)


def get_current_student():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role != 'student':
        return None, None
    return user, user.student_profile


@students_bp.route('/', methods=['GET'])
@jwt_required()
def list_students():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role not in ['admin', 'school', 'donor']:
        return jsonify({'error': 'Unauthorized'}), 403

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    state = request.args.get('state')
    degree = request.args.get('degree')

    query = Student.query.join(User).filter(User.is_active == True)
    if state:
        query = query.filter(Student.state == state)
    if degree:
        query = query.filter(Student.degree == degree)

    students = query.paginate(page=page, per_page=per_page, error_out=False)

    result = []
    for s in students.items:
        data = s.to_dict()
        data['full_name'] = f"{s.user.first_name or ''} {s.user.last_name or ''}".strip()
        data['email'] = s.user.email
        result.append(data)

    return jsonify({
        'students': result,
        'total': students.total,
        'pages': students.pages,
        'current_page': page,
    }), 200


@students_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    user, student = get_current_student()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404

    # Get applications
    apps = Application.query.filter_by(student_id=student.id).all()
    app_stats = {
        'total': len(apps),
        'submitted': sum(1 for a in apps if a.status == 'submitted'),
        'approved': sum(1 for a in apps if a.status == 'approved'),
        'rejected': sum(1 for a in apps if a.status == 'rejected'),
        'under_review': sum(1 for a in apps if a.status == 'under_review'),
    }

    # Get upcoming deadlines
    from datetime import date, timedelta
    upcoming = []
    for app in apps:
        s = app.scholarship
        if s and s.deadline and s.deadline >= date.today():
            days_left = (s.deadline - date.today()).days
            upcoming.append({
                'scholarship_name': s.name,
                'deadline': s.deadline.isoformat(),
                'days_left': days_left,
                'status': app.status,
            })
    upcoming.sort(key=lambda x: x['days_left'])

    # Get recent notifications
    notifications = Notification.query.filter_by(
        user_id=user.id
    ).order_by(Notification.created_at.desc()).limit(5).all()

    return jsonify({
        'student': student.to_dict(),
        'user': user.to_dict(),
        'application_stats': app_stats,
        'upcoming_deadlines': upcoming[:5],
        'notifications': [n.to_dict() for n in notifications],
        'financial_health_score': student.financial_health_score or 72,
        'dropout_risk': student.dropout_risk or 0.15,
        'profile_completion': student.profile_completion or 0,
    }), 200


@students_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user, student = get_current_student()
    if not student:
        return jsonify({'error': 'Student profile not found'}), 404
    data = student.to_dict()
    data['user'] = user.to_dict()
    return jsonify(data), 200


@students_bp.route('/<int:student_id>', methods=['GET'])
@jwt_required()
def get_student(student_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    student = Student.query.get_or_404(student_id)

    # Only admin, school, donor, or the student themselves can view
    if user.role not in ['admin', 'school', 'donor'] and student.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403

    data = student.to_dict()
    data['full_name'] = f"{student.user.first_name or ''} {student.user.last_name or ''}".strip()
    return jsonify(data), 200


@students_bp.route('/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    user, student = get_current_student()
    data = request.get_json() or {}

    # Use student profile or override with request data
    student_data = {
        'annual_income': data.get('annual_income', student.annual_income if student else 0) or 0,
        'cgpa': data.get('cgpa', student.cgpa if student else 0) or 0,
        'percentage': data.get('percentage', student.percentage if student else 0) or 0,
        'state': data.get('state', student.state if student else '') or '',
        'category': data.get('category', student.category if student else '') or '',
        'gender': data.get('gender', student.gender if student else '') or '',
        'degree': data.get('degree', student.degree if student else '') or '',
        'branch': data.get('branch', student.branch if student else '') or '',
        'disability_status': data.get('disability_status', student.disability_status if student else False),
        'achievements': data.get('achievements', student.achievements if student else '') or '',
        'skills': data.get('skills', student.skills if student else '') or '',
        'extracurricular': data.get('extracurricular', student.extracurricular if student else '') or '',
    }

    recommendations = recommend_scholarships(student_data)
    return jsonify({'recommendations': recommendations}), 200


@students_bp.route('/financial-health', methods=['POST'])
@jwt_required()
def get_financial_health():
    user, student = get_current_student()
    data = request.get_json() or {}

    student_data = {
        'annual_income': data.get('annual_income', student.annual_income if student else 0) or 0,
        'cgpa': data.get('cgpa', student.cgpa if student else 0) or 0,
        'attendance': data.get('attendance', student.attendance_percentage if student else 0) or 0,
        'fee_due': data.get('fee_due', student.fee_due if student else 0) or 0,
        'scholarship_received': data.get('scholarship_received', student.scholarship_amount_received if student else 0) or 0,
        'family_size': data.get('family_size', student.family_size if student else 4) or 4,
    }

    result = calculate_financial_health(student_data)

    # Update student record
    if student:
        student.financial_health_score = result['score']
        db.session.commit()

    return jsonify(result), 200


@students_bp.route('/dropout-risk', methods=['POST'])
@jwt_required()
def get_dropout_risk():
    user, student = get_current_student()
    data = request.get_json() or {}

    student_data = {
        'cgpa': data.get('cgpa', student.cgpa if student else 0) or 0,
        'attendance': data.get('attendance', student.attendance_percentage if student else 0) or 0,
        'annual_income': data.get('annual_income', student.annual_income if student else 0) or 0,
        'fee_due': data.get('fee_due', student.fee_due if student else 0) or 0,
        'year_of_study': data.get('year_of_study', student.year_of_study if student else 1) or 1,
        'family_size': data.get('family_size', student.family_size if student else 4) or 4,
    }

    result = predict_dropout_risk(student_data)

    if student:
        student.dropout_risk = result['dropout_probability']
        db.session.commit()

    return jsonify(result), 200
