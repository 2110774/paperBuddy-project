from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User, Student, ChatHistory, FundingPlan, CareerSuggestion
from app.ai.chatbot import get_chatbot_response
from app.ai.essay_generator import generate_essay
from app.ai.career import get_career_guidance
from app.ai.funding_planner import generate_funding_plan
from app.ai.financial_health import calculate_financial_health
from app.ai.dropout import predict_dropout_risk
from app.ai.recommendation import recommend_scholarships
import json

ai_bp = Blueprint('ai', __name__)


def get_student_profile(user_id):
    user = User.query.get(user_id)
    if user and user.student_profile:
        return user, user.student_profile
    return user, None


@ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def chat():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Message is required'}), 400

    result = get_chatbot_response(message)

    # Save to chat history
    user, student = get_student_profile(user_id)
    if student:
        history = ChatHistory(
            student_id=student.id,
            user_message=message,
            bot_response=result['response'],
            intent=result.get('intent', 'unknown'),
            confidence=result.get('confidence', 0),
        )
        db.session.add(history)
        db.session.commit()

    return jsonify(result), 200


@ai_bp.route('/chat/history', methods=['GET'])
@jwt_required()
def chat_history():
    user_id = int(get_jwt_identity())
    user, student = get_student_profile(user_id)
    if not student:
        return jsonify({'history': []}), 200

    history = ChatHistory.query.filter_by(
        student_id=student.id
    ).order_by(ChatHistory.created_at.asc()).limit(50).all()

    return jsonify({'history': [h.to_dict() for h in history]}), 200


@ai_bp.route('/essay', methods=['POST'])
@jwt_required()
def generate_essay_route():
    user_id = int(get_jwt_identity())
    user, student = get_student_profile(user_id)
    data = request.get_json()

    context = {
        'name': f"{user.first_name} {user.last_name}".strip() if user else 'Student',
        'year_of_study': student.year_of_study if student else 1,
        'degree': student.degree if student else '',
        'branch': student.branch if student else '',
        'institution': student.institution_name if student else '',
        'state': student.state if student else '',
        'annual_income': student.annual_income if student else 0,
        'cgpa': student.cgpa if student else 0,
        'achievements': student.achievements if student else '',
        'scholarship_name': data.get('scholarship_name', 'this scholarship'),
        'purpose': data.get('purpose', 'cover tuition fees and focus on studies'),
        'career_goal': data.get('career_goal', 'my chosen field'),
    }

    essay_type = data.get('essay_type', 'scholarship_essay')
    result = generate_essay(essay_type, context)
    return jsonify(result), 200


@ai_bp.route('/career', methods=['POST'])
@jwt_required()
def career_guidance():
    user_id = int(get_jwt_identity())
    user, student = get_student_profile(user_id)
    data = request.get_json() or {}

    student_data = {
        'branch': data.get('branch', student.branch if student else '') or '',
        'cgpa': data.get('cgpa', student.cgpa if student else 0) or 0,
        'interests': data.get('interests', student.interests if student else '') or '',
        'skills': data.get('skills', student.skills if student else '') or '',
        'annual_income': data.get('annual_income', student.annual_income if student else 0) or 0,
        'degree': data.get('degree', student.degree if student else '') or '',
    }

    result = get_career_guidance(student_data)

    # Save suggestion
    if student:
        suggestion = CareerSuggestion(
            student_id=student.id,
            careers=json.dumps(result['careers']),
            courses=json.dumps(result['courses']),
            internships=json.dumps(result['internships']),
            skills_to_develop=json.dumps(result['skills_to_develop']),
            confidence_score=result['confidence_score'],
        )
        db.session.add(suggestion)
        db.session.commit()

    return jsonify(result), 200


@ai_bp.route('/funding-plan', methods=['POST'])
@jwt_required()
def funding_plan():
    user_id = int(get_jwt_identity())
    user, student = get_student_profile(user_id)
    data = request.get_json() or {}

    total_fee = data.get('total_fee', 100000)

    student_data = {
        'annual_income': data.get('annual_income', student.annual_income if student else 0) or 0,
        'cgpa': data.get('cgpa', student.cgpa if student else 0) or 0,
        'category': data.get('category', student.category if student else '') or '',
        'disability_status': data.get('disability_status', student.disability_status if student else False),
        'state': data.get('state', student.state if student else '') or '',
        'degree': data.get('degree', student.degree if student else '') or '',
    }

    plan = generate_funding_plan(student_data, total_fee)

    # Save plan
    if student:
        fp = FundingPlan(
            student_id=student.id,
            total_fee=total_fee,
            government_scholarship=plan['government_scholarship'],
            csr_funding=plan['csr_funding'],
            ngo_funding=plan['ngo_funding'],
            loan_amount=plan['loan_amount'],
            crowdfunding=plan['crowdfunding'],
            installments=plan['installments'],
            funding_gap=plan['funding_gap'],
            plan_data=json.dumps(plan),
        )
        db.session.add(fp)
        db.session.commit()

    return jsonify(plan), 200


@ai_bp.route('/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    user_id = int(get_jwt_identity())
    user, student = get_student_profile(user_id)
    data = request.get_json() or {}

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
    }

    recommendations = recommend_scholarships(student_data)
    return jsonify({'recommendations': recommendations, 'total': len(recommendations)}), 200


@ai_bp.route('/financial-health', methods=['POST'])
@jwt_required()
def financial_health():
    user_id = int(get_jwt_identity())
    user, student = get_student_profile(user_id)
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
    return jsonify(result), 200


@ai_bp.route('/dropout-risk', methods=['POST'])
@jwt_required()
def dropout_risk():
    user_id = int(get_jwt_identity())
    user, student = get_student_profile(user_id)
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
    return jsonify(result), 200
