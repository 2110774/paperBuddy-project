from app import db
from datetime import datetime
import json


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    # role: student | parent | school | ngo | csr | donor | admin
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(256))
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(128))
    reset_token = db.Column(db.String(128))
    reset_token_expiry = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    student_profile = db.relationship('Student', backref='user', uselist=False, lazy=True)
    parent_profile = db.relationship('Parent', backref='user', uselist=False, lazy=True)
    school_profile = db.relationship('School', backref='user', uselist=False, lazy=True)
    donor_profile = db.relationship('Donor', backref='user', uselist=False, lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)
    audit_logs = db.relationship('AuditLog', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name or ''} {self.last_name or ''}".strip(),
            'phone': self.phone,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_id = db.Column(db.String(20), unique=True)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    category = db.Column(db.String(20))  # General/OBC/SC/ST/EWS
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    address = db.Column(db.Text)
    degree = db.Column(db.String(50))
    branch = db.Column(db.String(100))
    year_of_study = db.Column(db.Integer)
    institution_name = db.Column(db.String(200))
    cgpa = db.Column(db.Float)
    percentage = db.Column(db.Float)
    annual_income = db.Column(db.Float)
    family_size = db.Column(db.Integer)
    disability_status = db.Column(db.Boolean, default=False)
    disability_type = db.Column(db.String(100))
    achievements = db.Column(db.Text)
    skills = db.Column(db.Text)
    extracurricular = db.Column(db.Text)
    interests = db.Column(db.Text)
    financial_health_score = db.Column(db.Float)
    dropout_risk = db.Column(db.Float)
    profile_completion = db.Column(db.Integer, default=0)
    attendance_percentage = db.Column(db.Float)
    fee_due = db.Column(db.Float, default=0)
    scholarship_amount_received = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='student', lazy=True)
    documents = db.relationship('Document', backref='student', lazy=True)
    funding_plans = db.relationship('FundingPlan', backref='student', lazy=True)
    career_suggestions = db.relationship('CareerSuggestion', backref='student', lazy=True)
    chat_history = db.relationship('ChatHistory', backref='student', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_id': self.student_id,
            'gender': self.gender,
            'category': self.category,
            'state': self.state,
            'city': self.city,
            'degree': self.degree,
            'branch': self.branch,
            'year_of_study': self.year_of_study,
            'institution_name': self.institution_name,
            'cgpa': self.cgpa,
            'percentage': self.percentage,
            'annual_income': self.annual_income,
            'family_size': self.family_size,
            'disability_status': self.disability_status,
            'achievements': self.achievements,
            'skills': self.skills,
            'extracurricular': self.extracurricular,
            'interests': self.interests,
            'financial_health_score': self.financial_health_score,
            'dropout_risk': self.dropout_risk,
            'profile_completion': self.profile_completion,
            'attendance_percentage': self.attendance_percentage,
            'fee_due': self.fee_due,
            'scholarship_amount_received': self.scholarship_amount_received,
        }


class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    annual_income = db.Column(db.Float)
    occupation = db.Column(db.String(100))
    relationship_to_student = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'student_id': self.student_id,
            'annual_income': self.annual_income,
            'occupation': self.occupation,
            'relationship_to_student': self.relationship_to_student,
        }


class School(db.Model):
    __tablename__ = 'schools'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(20), unique=True)
    type = db.Column(db.String(50))  # University/College/School
    affiliation = db.Column(db.String(200))
    state = db.Column(db.String(50))
    city = db.Column(db.String(50))
    address = db.Column(db.Text)
    website = db.Column(db.String(256))
    total_students = db.Column(db.Integer)
    scholarship_budget = db.Column(db.Float)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'code': self.code,
            'type': self.type,
            'state': self.state,
            'city': self.city,
            'total_students': self.total_students,
            'is_verified': self.is_verified,
        }


class Donor(db.Model):
    __tablename__ = 'donors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(20))  # individual | ngo | csr | alumni
    organization_name = db.Column(db.String(200))
    total_donated = db.Column(db.Float, default=0)
    students_supported = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    donations = db.relationship('Donation', backref='donor', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'organization_name': self.organization_name,
            'total_donated': self.total_donated,
            'students_supported': self.students_supported,
        }


class Scholarship(db.Model):
    __tablename__ = 'scholarships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    provider = db.Column(db.String(200))
    type = db.Column(db.String(50))  # government | ngo | csr | alumni | crowdfunding | loan | emergency
    description = db.Column(db.Text)
    amount = db.Column(db.Float)
    min_amount = db.Column(db.Float)
    max_amount = db.Column(db.Float)
    deadline = db.Column(db.Date)
    eligible_degrees = db.Column(db.Text)  # JSON list
    eligible_states = db.Column(db.Text)   # JSON list
    eligible_categories = db.Column(db.Text)  # JSON list
    eligible_genders = db.Column(db.Text)
    min_cgpa = db.Column(db.Float, default=0)
    max_income = db.Column(db.Float)
    min_percentage = db.Column(db.Float, default=0)
    disability_only = db.Column(db.Boolean, default=False)
    documents_required = db.Column(db.Text)  # JSON list
    application_url = db.Column(db.String(512))
    is_active = db.Column(db.Boolean, default=True)
    total_seats = db.Column(db.Integer)
    filled_seats = db.Column(db.Integer, default=0)
    renewal_possible = db.Column(db.Boolean, default=False)
    tags = db.Column(db.Text)  # JSON list
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship('Application', backref='scholarship', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
            'type': self.type,
            'description': self.description,
            'amount': self.amount,
            'min_amount': self.min_amount,
            'max_amount': self.max_amount,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'eligible_degrees': json.loads(self.eligible_degrees) if self.eligible_degrees else [],
            'eligible_states': json.loads(self.eligible_states) if self.eligible_states else [],
            'eligible_categories': json.loads(self.eligible_categories) if self.eligible_categories else [],
            'min_cgpa': self.min_cgpa,
            'max_income': self.max_income,
            'min_percentage': self.min_percentage,
            'disability_only': self.disability_only,
            'documents_required': json.loads(self.documents_required) if self.documents_required else [],
            'is_active': self.is_active,
            'total_seats': self.total_seats,
            'filled_seats': self.filled_seats,
            'tags': json.loads(self.tags) if self.tags else [],
        }


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id'), nullable=False)
    status = db.Column(db.String(30), default='draft')
    # draft | submitted | under_review | approved | rejected | disbursed
    fit_score = db.Column(db.Float)
    selection_probability = db.Column(db.Float)
    essay = db.Column(db.Text)
    notes = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime)
    reviewed_at = db.Column(db.DateTime)
    reviewer_notes = db.Column(db.Text)
    amount_approved = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'scholarship_id': self.scholarship_id,
            'status': self.status,
            'fit_score': self.fit_score,
            'selection_probability': self.selection_probability,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'amount_approved': self.amount_approved,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    type = db.Column(db.String(50))
    # income_certificate | marksheet | identity | bank_passbook | bonafide
    filename = db.Column(db.String(256))
    file_path = db.Column(db.String(512))
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(50))
    ocr_status = db.Column(db.String(20), default='pending')
    # pending | processing | verified | rejected
    ocr_data = db.Column(db.Text)  # JSON extracted data
    ocr_score = db.Column(db.Float)
    fraud_score = db.Column(db.Float)
    fraud_flags = db.Column(db.Text)  # JSON flags list
    is_verified = db.Column(db.Boolean, default=False)
    rejection_reason = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'type': self.type,
            'filename': self.filename,
            'ocr_status': self.ocr_status,
            'ocr_score': self.ocr_score,
            'fraud_score': self.fraud_score,
            'fraud_flags': json.loads(self.fraud_flags) if self.fraud_flags else [],
            'is_verified': self.is_verified,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
        }


class Donation(db.Model):
    __tablename__ = 'donations'

    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id'))
    amount = db.Column(db.Float, nullable=False)
    purpose = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')
    # pending | completed | refunded
    transaction_id = db.Column(db.String(100))
    certificate_url = db.Column(db.String(512))
    donated_at = db.Column(db.DateTime, default=datetime.utcnow)
    impact_report = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'student_id': self.student_id,
            'scholarship_id': self.scholarship_id,
            'amount': self.amount,
            'purpose': self.purpose,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'donated_at': self.donated_at.isoformat() if self.donated_at else None,
        }


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(30))  # fee | scholarship | donation | refund
    status = db.Column(db.String(20), default='pending')
    gateway = db.Column(db.String(50))
    transaction_id = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'type': self.type,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    type = db.Column(db.String(30))
    # scholarship | payment | application | alert | system
    is_read = db.Column(db.Boolean, default=False)
    action_url = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'action_url': self.action_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class FundingPlan(db.Model):
    __tablename__ = 'funding_plans'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    total_fee = db.Column(db.Float)
    government_scholarship = db.Column(db.Float, default=0)
    csr_funding = db.Column(db.Float, default=0)
    ngo_funding = db.Column(db.Float, default=0)
    loan_amount = db.Column(db.Float, default=0)
    crowdfunding = db.Column(db.Float, default=0)
    installments = db.Column(db.Float, default=0)
    funding_gap = db.Column(db.Float, default=0)
    plan_data = db.Column(db.Text)  # JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'total_fee': self.total_fee,
            'government_scholarship': self.government_scholarship,
            'csr_funding': self.csr_funding,
            'ngo_funding': self.ngo_funding,
            'loan_amount': self.loan_amount,
            'crowdfunding': self.crowdfunding,
            'installments': self.installments,
            'funding_gap': self.funding_gap,
        }


class CareerSuggestion(db.Model):
    __tablename__ = 'career_suggestions'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    careers = db.Column(db.Text)  # JSON list
    courses = db.Column(db.Text)  # JSON list
    internships = db.Column(db.Text)  # JSON list
    skills_to_develop = db.Column(db.Text)  # JSON list
    confidence_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'careers': json.loads(self.careers) if self.careers else [],
            'courses': json.loads(self.courses) if self.courses else [],
            'internships': json.loads(self.internships) if self.internships else [],
            'skills_to_develop': json.loads(self.skills_to_develop) if self.skills_to_develop else [],
            'confidence_score': self.confidence_score,
        }


class AIReport(db.Model):
    __tablename__ = 'ai_reports'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    type = db.Column(db.String(50))
    # financial_health | dropout_risk | recommendation | fraud
    data = db.Column(db.Text)  # JSON
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'type': self.type,
            'data': json.loads(self.data) if self.data else {},
            'score': self.score,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100))
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    ip_address = db.Column(db.String(45))
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    user_message = db.Column(db.Text)
    bot_response = db.Column(db.Text)
    intent = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'user_message': self.user_message,
            'bot_response': self.bot_response,
            'intent': self.intent,
            'confidence': self.confidence,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
