from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import School, User, Student, Application

schools_bp = Blueprint('schools', __name__)


@schools_bp.route('/', methods=['GET'])
def list_schools():
    schools = School.query.filter_by(is_verified=True).all()
    return jsonify({'schools': [s.to_dict() for s in schools]}), 200


@schools_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def school_dashboard():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role != 'school' or not user.school_profile:
        return jsonify({'error': 'School profile not found'}), 404

    school = user.school_profile

    # For demo: aggregate some stats
    total_applications = Application.query.count()
    pending = Application.query.filter_by(status='submitted').count()
    approved = Application.query.filter_by(status='approved').count()

    return jsonify({
        'school': school.to_dict(),
        'stats': {
            'total_students': school.total_students or 0,
            'total_applications': total_applications,
            'pending_review': pending,
            'approved': approved,
            'scholarship_budget': school.scholarship_budget or 0,
        }
    }), 200


@schools_bp.route('/<int:school_id>', methods=['GET'])
def get_school(school_id):
    school = School.query.get_or_404(school_id)
    return jsonify(school.to_dict()), 200
