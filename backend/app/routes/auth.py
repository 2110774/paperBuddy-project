from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app import db, bcrypt
from app.models import User, Student, Parent, School, Donor, AuditLog
from datetime import datetime, timedelta
import secrets
import random
import string

auth_bp = Blueprint('auth', __name__)


def generate_token(length=32):
    return secrets.token_urlsafe(length)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email', '').lower().strip()
    password = data.get('password', '')
    role = data.get('role', 'student')
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 409

    valid_roles = ['student', 'parent', 'school', 'ngo', 'csr', 'donor', 'admin']
    if role not in valid_roles:
        role = 'student'

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    verification_token = generate_token()

    user = User(
        email=email,
        password_hash=password_hash,
        role=role,
        first_name=first_name,
        last_name=last_name,
        verification_token=verification_token,
        is_verified=True,  # Auto-verify for demo
    )
    db.session.add(user)
    db.session.flush()

    # Create role-specific profile
    if role == 'student':
        student_id = 'STU' + ''.join(random.choices(string.digits, k=6))
        profile = Student(
            user_id=user.id,
            student_id=student_id,
            profile_completion=20,
        )
        db.session.add(profile)
    elif role == 'parent':
        profile = Parent(user_id=user.id)
        db.session.add(profile)
    elif role == 'school':
        school_code = 'SCH' + ''.join(random.choices(string.digits, k=4))
        name = data.get('organization_name', f"{first_name}'s Institution")
        profile = School(user_id=user.id, name=name, code=school_code)
        db.session.add(profile)
    elif role in ['donor', 'ngo', 'csr']:
        profile = Donor(
            user_id=user.id,
            type=role,
            organization_name=data.get('organization_name', ''),
        )
        db.session.add(profile)

    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        'message': 'Registration successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(),
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    email = data.get('email', '').lower().strip()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403

    user.last_login = datetime.utcnow()
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    # Get profile based on role
    profile = None
    if user.role == 'student' and user.student_profile:
        profile = user.student_profile.to_dict()
    elif user.role == 'school' and user.school_profile:
        profile = user.school_profile.to_dict()
    elif user.role == 'donor' and user.donor_profile:
        profile = user.donor_profile.to_dict()

    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict(),
        'profile': profile,
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({'access_token': access_token}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    profile = None
    if user.role == 'student' and user.student_profile:
        profile = user.student_profile.to_dict()
    elif user.role == 'school' and user.school_profile:
        profile = user.school_profile.to_dict()
    elif user.role == 'donor' and user.donor_profile:
        profile = user.donor_profile.to_dict()
    return jsonify({'user': user.to_dict(), 'profile': profile}), 200


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email', '').lower().strip()
    user = User.query.filter_by(email=email).first()

    # Always return success for security
    if user:
        reset_token = generate_token()
        user.reset_token = reset_token
        user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
        db.session.commit()
        # In production: send email with reset link
        # For demo: return token in response
        return jsonify({
            'message': 'Password reset link sent to your email',
            'demo_token': reset_token  # Only for demo
        }), 200

    return jsonify({'message': 'If that email exists, a reset link has been sent'}), 200


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')

    if not token or not new_password:
        return jsonify({'error': 'Token and password required'}), 400

    user = User.query.filter_by(reset_token=token).first()
    if not user or not user.reset_token_expiry or user.reset_token_expiry < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    user.password_hash = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    return jsonify({'message': 'Password reset successfully'}), 200


@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'phone' in data:
        user.phone = data['phone']

    # Update student profile fields
    if user.role == 'student' and user.student_profile:
        s = user.student_profile
        fields = ['cgpa', 'percentage', 'annual_income', 'state', 'city', 'degree',
                  'branch', 'year_of_study', 'institution_name', 'gender', 'category',
                  'disability_status', 'achievements', 'skills', 'extracurricular',
                  'interests', 'family_size', 'attendance_percentage', 'fee_due']
        for field in fields:
            if field in data:
                setattr(s, field, data[field])
        # Recalculate profile completion
        completed = sum(1 for f in ['cgpa', 'annual_income', 'state', 'degree', 'branch',
                                     'gender', 'category', 'institution_name', 'year_of_study']
                        if getattr(s, f))
        s.profile_completion = min(100, 20 + completed * 8)

    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200
