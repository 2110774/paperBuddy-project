from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Scholarship, User
import json
from datetime import date

scholarships_bp = Blueprint('scholarships', __name__)


@scholarships_bp.route('/', methods=['GET'])
def list_scholarships():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    type_filter = request.args.get('type', '')
    state_filter = request.args.get('state', '')
    degree_filter = request.args.get('degree', '')
    min_amount = request.args.get('min_amount', type=float)
    max_income = request.args.get('max_income', type=float)

    query = Scholarship.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            Scholarship.name.contains(search) |
            Scholarship.provider.contains(search) |
            Scholarship.description.contains(search)
        )
    if type_filter:
        query = query.filter(Scholarship.type == type_filter)
    if min_amount:
        query = query.filter(Scholarship.amount >= min_amount)
    if max_income:
        query = query.filter(Scholarship.max_income >= max_income)

    scholarships = query.order_by(Scholarship.deadline.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    result = []
    for s in scholarships.items:
        d = s.to_dict()
        if s.deadline:
            d['days_left'] = (s.deadline - date.today()).days
        result.append(d)

    return jsonify({
        'scholarships': result,
        'total': scholarships.total,
        'pages': scholarships.pages,
        'current_page': page,
    }), 200


@scholarships_bp.route('/<int:scholarship_id>', methods=['GET'])
def get_scholarship(scholarship_id):
    s = Scholarship.query.get_or_404(scholarship_id)
    data = s.to_dict()
    if s.deadline:
        data['days_left'] = (s.deadline - date.today()).days
    return jsonify(data), 200


@scholarships_bp.route('/', methods=['POST'])
@jwt_required()
def create_scholarship():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role not in ['admin', 'school']:
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    s = Scholarship(
        name=data['name'],
        provider=data.get('provider', ''),
        type=data.get('type', 'government'),
        description=data.get('description', ''),
        amount=data.get('amount'),
        min_amount=data.get('min_amount'),
        max_amount=data.get('max_amount'),
        max_income=data.get('max_income'),
        min_cgpa=data.get('min_cgpa', 0),
        min_percentage=data.get('min_percentage', 0),
        eligible_degrees=json.dumps(data.get('eligible_degrees', [])),
        eligible_states=json.dumps(data.get('eligible_states', [])),
        eligible_categories=json.dumps(data.get('eligible_categories', [])),
        eligible_genders=json.dumps(data.get('eligible_genders', [])),
        disability_only=data.get('disability_only', False),
        documents_required=json.dumps(data.get('documents_required', [])),
        tags=json.dumps(data.get('tags', [])),
        total_seats=data.get('total_seats'),
        renewal_possible=data.get('renewal_possible', False),
    )

    if data.get('deadline'):
        from datetime import datetime
        s.deadline = datetime.strptime(data['deadline'], '%Y-%m-%d').date()

    db.session.add(s)
    db.session.commit()
    return jsonify({'message': 'Scholarship created', 'scholarship': s.to_dict()}), 201


@scholarships_bp.route('/<int:scholarship_id>', methods=['PUT'])
@jwt_required()
def update_scholarship(scholarship_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    s = Scholarship.query.get_or_404(scholarship_id)
    data = request.get_json()

    for field in ['name', 'provider', 'type', 'description', 'amount', 'min_amount',
                  'max_amount', 'max_income', 'min_cgpa', 'min_percentage', 'disability_only',
                  'total_seats', 'renewal_possible', 'is_active']:
        if field in data:
            setattr(s, field, data[field])

    for json_field in ['eligible_degrees', 'eligible_states', 'eligible_categories',
                       'eligible_genders', 'documents_required', 'tags']:
        if json_field in data:
            setattr(s, json_field, json.dumps(data[json_field]))

    db.session.commit()
    return jsonify({'message': 'Updated', 'scholarship': s.to_dict()}), 200


@scholarships_bp.route('/stats', methods=['GET'])
def get_stats():
    total = Scholarship.query.filter_by(is_active=True).count()
    by_type = db.session.query(Scholarship.type, db.func.count(Scholarship.id)) \
        .filter_by(is_active=True).group_by(Scholarship.type).all()
    return jsonify({
        'total': total,
        'by_type': {t: c for t, c in by_type},
    }), 200
