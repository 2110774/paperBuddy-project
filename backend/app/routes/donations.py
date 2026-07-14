from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Donor, Student, Donation

donations_bp = Blueprint('donations', __name__)


@donations_bp.route('/', methods=['GET'])
@jwt_required()
def list_donations():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if user.role in ['donor', 'ngo', 'csr'] and user.donor_profile:
        donations = Donation.query.filter_by(donor_id=user.donor_profile.id).all()
    elif user.role == 'admin':
        donations = Donation.query.order_by(Donation.donated_at.desc()).limit(100).all()
    else:
        return jsonify({'donations': []}), 200

    result = []
    for d in donations:
        data = d.to_dict()
        if d.student_id:
            s = Student.query.get(d.student_id)
            if s and s.user:
                data['student_name'] = f"{s.user.first_name} {s.user.last_name}".strip()
        result.append(data)

    return jsonify({'donations': result}), 200


@donations_bp.route('/', methods=['POST'])
@jwt_required()
def create_donation():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role not in ['donor', 'ngo', 'csr', 'admin']:
        return jsonify({'error': 'Only donors can make donations'}), 403

    data = request.get_json()
    amount = data.get('amount', 0)
    if amount <= 0:
        return jsonify({'error': 'Invalid amount'}), 400

    donor = user.donor_profile
    if not donor:
        return jsonify({'error': 'Donor profile not found'}), 404

    import uuid
    donation = Donation(
        donor_id=donor.id,
        student_id=data.get('student_id'),
        scholarship_id=data.get('scholarship_id'),
        amount=amount,
        purpose=data.get('purpose', 'General scholarship support'),
        status='completed',
        transaction_id=str(uuid.uuid4())[:12].upper(),
    )
    db.session.add(donation)

    donor.total_donated = (donor.total_donated or 0) + amount
    if data.get('student_id'):
        donor.students_supported = (donor.students_supported or 0) + 1

    db.session.commit()
    return jsonify({'message': 'Donation successful', 'donation': donation.to_dict()}), 201


@donations_bp.route('/impact', methods=['GET'])
@jwt_required()
def get_impact():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or not user.donor_profile:
        return jsonify({'error': 'Donor profile not found'}), 404

    donor = user.donor_profile
    donations = Donation.query.filter_by(donor_id=donor.id, status='completed').all()
    total = sum(d.amount for d in donations)
    students_count = len(set(d.student_id for d in donations if d.student_id))

    return jsonify({
        'total_donated': total,
        'donation_count': len(donations),
        'students_supported': students_count,
        'impact': {
            'meals_provided': int(total / 30),
            'months_education': int(total / 5000),
            'books_provided': int(total / 500),
        }
    }), 200
