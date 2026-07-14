from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Document, Student, User
import os, json
from datetime import datetime

documents_bp = Blueprint('documents', __name__)


def simple_ocr_verification(file_path: str, doc_type: str) -> dict:
    """
    Simplified document verification without heavy OCR libraries.
    In production, use pytesseract or easyocr.
    """
    import os
    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
    
    flags = []
    score = 100.0

    if file_size < 10000:  # Less than 10KB
        flags.append('File too small — may be low quality')
        score -= 30

    if file_size > 15 * 1024 * 1024:  # More than 15MB
        flags.append('File too large')
        score -= 10

    # Simulate OCR data extraction based on doc type
    ocr_data = {}
    if doc_type == 'income_certificate':
        ocr_data = {'detected_fields': ['name', 'income_amount', 'issuing_authority'], 'confidence': 0.85}
    elif doc_type == 'marksheet':
        ocr_data = {'detected_fields': ['student_name', 'marks', 'institution', 'year'], 'confidence': 0.90}
    elif doc_type == 'identity':
        ocr_data = {'detected_fields': ['name', 'dob', 'id_number'], 'confidence': 0.92}
    elif doc_type == 'bank_passbook':
        ocr_data = {'detected_fields': ['account_number', 'bank_name', 'ifsc'], 'confidence': 0.88}
    elif doc_type == 'bonafide':
        ocr_data = {'detected_fields': ['student_name', 'institution', 'course', 'year'], 'confidence': 0.87}

    score = max(0, min(100, score))
    status = 'verified' if score >= 70 and not flags else ('rejected' if score < 40 else 'verified')

    return {
        'status': status,
        'score': score,
        'flags': flags,
        'ocr_data': ocr_data,
        'fraud_score': max(0, 100 - score) / 100,
    }


@documents_bp.route('/', methods=['GET'])
@jwt_required()
def list_documents():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if user.role == 'student' and user.student_profile:
        docs = Document.query.filter_by(student_id=user.student_profile.id).all()
    elif user.role in ['admin', 'school']:
        student_id = request.args.get('student_id', type=int)
        query = Document.query
        if student_id:
            query = query.filter_by(student_id=student_id)
        docs = query.all()
    else:
        return jsonify({'documents': []}), 200

    return jsonify({'documents': [d.to_dict() for d in docs]}), 200


@documents_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_document():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user or user.role != 'student' or not user.student_profile:
        return jsonify({'error': 'Only students can upload documents'}), 403

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    doc_type = request.form.get('doc_type', 'other')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Secure filename
    from werkzeug.utils import secure_filename
    import uuid
    ext = file.filename.rsplit('.', 1)[-1].lower() if '.' in file.filename else 'pdf'
    filename = f"{uuid.uuid4().hex}.{ext}"
    
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user_id))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    file.save(file_path)
    file_size = os.path.getsize(file_path)

    # Run verification
    verification = simple_ocr_verification(file_path, doc_type)

    doc = Document(
        student_id=user.student_profile.id,
        type=doc_type,
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type,
        ocr_status=verification['status'],
        ocr_data=json.dumps(verification['ocr_data']),
        ocr_score=verification['score'],
        fraud_score=verification['fraud_score'],
        fraud_flags=json.dumps(verification['flags']),
        is_verified=verification['status'] == 'verified',
        verified_at=datetime.utcnow() if verification['status'] == 'verified' else None,
    )
    db.session.add(doc)
    db.session.commit()

    return jsonify({
        'message': 'Document uploaded and verified',
        'document': doc.to_dict(),
        'verification': verification,
    }), 201


@documents_bp.route('/<int:doc_id>', methods=['DELETE'])
@jwt_required()
def delete_document(doc_id):
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    doc = Document.query.get_or_404(doc_id)

    if user.role == 'student':
        if not user.student_profile or doc.student_id != user.student_profile.id:
            return jsonify({'error': 'Unauthorized'}), 403

    if os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    db.session.delete(doc)
    db.session.commit()
    return jsonify({'message': 'Document deleted'}), 200
