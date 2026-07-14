from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Student, School, Scholarship, Application, Donation, Payment, AuditLog
from datetime import datetime, timedelta
import random

admin_bp = Blueprint('admin', __name__)


def require_admin():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return None
    return user


@admin_bp.route('/stats', methods=['GET'])
@jwt_required()
def platform_stats():
    admin = require_admin()
    if not admin:
        return jsonify({'error': 'Unauthorized'}), 403

    total_users = User.query.count()
    total_students = Student.query.count()
    total_schools = School.query.count()
    total_scholarships = Scholarship.query.filter_by(is_active=True).count()
    total_applications = Application.query.count()
    approved_applications = Application.query.filter_by(status='approved').count()
    total_donations = db.session.query(db.func.sum(Donation.amount)).filter_by(status='completed').scalar() or 0

    # Recent stats (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users = User.query.filter(User.created_at >= thirty_days_ago).count()
    new_applications = Application.query.filter(Application.created_at >= thirty_days_ago).count()

    # Applications by status
    app_by_status = db.session.query(
        Application.status, db.func.count(Application.id)
    ).group_by(Application.status).all()

    # Users by role
    users_by_role = db.session.query(
        User.role, db.func.count(User.id)
    ).group_by(User.role).all()

    # Monthly applications (last 6 months)
    monthly_data = []
    for i in range(5, -1, -1):
        start = datetime.utcnow() - timedelta(days=30 * (i + 1))
        end = datetime.utcnow() - timedelta(days=30 * i)
        count = Application.query.filter(
            Application.created_at >= start,
            Application.created_at < end
        ).count()
        monthly_data.append({
            'month': start.strftime('%b'),
            'applications': count
        })

    return jsonify({
        'overview': {
            'total_users': total_users,
            'total_students': total_students,
            'total_schools': total_schools,
            'total_scholarships': total_scholarships,
            'total_applications': total_applications,
            'approved_applications': approved_applications,
            'total_donations': round(total_donations),
            'new_users_30d': new_users,
            'new_applications_30d': new_applications,
        },
        'applications_by_status': {s: c for s, c in app_by_status},
        'users_by_role': {r: c for r, c in users_by_role},
        'monthly_applications': monthly_data,
    }), 200


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    admin = require_admin()
    if not admin:
        return jsonify({'error': 'Unauthorized'}), 403

    page = request.args.get('page', 1, type=int)
    role = request.args.get('role')
    search = request.args.get('search')

    query = User.query
    if role:
        query = query.filter_by(role=role)
    if search:
        query = query.filter(
            User.email.contains(search) |
            User.first_name.contains(search) |
            User.last_name.contains(search)
        )

    users = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return jsonify({
        'users': [u.to_dict() for u in users.items],
        'total': users.total,
        'pages': users.pages,
    }), 200


@admin_bp.route('/users/<int:user_id>/toggle', methods=['PUT'])
@jwt_required()
def toggle_user(user_id):
    admin = require_admin()
    if not admin:
        return jsonify({'error': 'Unauthorized'}), 403

    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({'message': f'User {"activated" if user.is_active else "deactivated"}', 'user': user.to_dict()}), 200


@admin_bp.route('/scholarships', methods=['GET'])
@jwt_required()
def admin_scholarships():
    admin = require_admin()
    if not admin:
        return jsonify({'error': 'Unauthorized'}), 403

    scholarships = Scholarship.query.order_by(Scholarship.created_at.desc()).limit(100).all()
    return jsonify({'scholarships': [s.to_dict() for s in scholarships]}), 200


@admin_bp.route('/applications', methods=['GET'])
@jwt_required()
def admin_applications():
    admin = require_admin()
    if not admin:
        return jsonify({'error': 'Unauthorized'}), 403

    page = request.args.get('page', 1, type=int)
    status = request.args.get('status')

    query = Application.query
    if status:
        query = query.filter_by(status=status)

    apps = query.order_by(Application.created_at.desc()).paginate(page=page, per_page=20, error_out=False)

    result = []
    for app in apps.items:
        d = app.to_dict()
        if app.scholarship:
            d['scholarship_name'] = app.scholarship.name
        if app.student and app.student.user:
            d['student_name'] = f"{app.student.user.first_name} {app.student.user.last_name}".strip()
        result.append(d)

    return jsonify({
        'applications': result,
        'total': apps.total,
        'pages': apps.pages,
    }), 200


@admin_bp.route('/fraud-detection', methods=['GET'])
@jwt_required()
def fraud_detection():
    admin = require_admin()
    if not admin:
        return jsonify({'error': 'Unauthorized'}), 403

    # Detect duplicate applications (same student, multiple scholarships on same day)
    from sqlalchemy import func, text
    
    # Students with many applications (potential fraud)
    suspicious = db.session.query(
        Application.student_id,
        func.count(Application.id).label('app_count')
    ).group_by(Application.student_id).having(func.count(Application.id) > 10).all()

    fraud_alerts = []
    for student_id, count in suspicious:
        student = Student.query.get(student_id)
        if student and student.user:
            fraud_alerts.append({
                'type': 'multiple_applications',
                'student_id': student_id,
                'student_name': f"{student.user.first_name} {student.user.last_name}".strip(),
                'count': count,
                'risk': 'medium' if count <= 15 else 'high',
                'description': f'Student has submitted {count} applications',
            })

    return jsonify({
        'fraud_alerts': fraud_alerts,
        'total_flagged': len(fraud_alerts),
        'summary': {
            'high_risk': sum(1 for a in fraud_alerts if a['risk'] == 'high'),
            'medium_risk': sum(1 for a in fraud_alerts if a['risk'] == 'medium'),
        }
    }), 200
