"""
EduBridge AI — Database Seed Script
Generates: 5 demo accounts, 200 scholarships, 100 students, 20 schools, 50 donations
Run: python seed.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db, bcrypt
from app.models import (User, Student, Parent, School, Donor, Scholarship,
                        Application, Donation, Notification, FundingPlan, Payment)
from datetime import datetime, date, timedelta
import random
import json
import string

app = create_app()

STATES = ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh', 'Rajasthan',
          'Gujarat', 'West Bengal', 'Madhya Pradesh', 'Bihar', 'Odisha',
          'Andhra Pradesh', 'Telangana', 'Punjab', 'Haryana', 'Kerala']

DEGREES = ['B.Tech', 'B.E.', 'B.Sc', 'B.Com', 'BBA', 'B.A.', 'MBBS', 'B.Pharm', 'Diploma', 'M.Tech', 'MBA', 'M.Sc']

BRANCHES = ['Computer Science', 'Electronics', 'Mechanical', 'Civil', 'Chemical',
            'Information Technology', 'Electrical', 'Biotechnology', 'Data Science',
            'AI & ML', 'Commerce', 'Arts', 'Physics', 'Chemistry', 'Mathematics']

CATEGORIES = ['General', 'OBC', 'SC', 'ST', 'EWS']
GENDERS = ['Male', 'Female', 'Other']

FIRST_NAMES = ['Aarav', 'Priya', 'Rahul', 'Ananya', 'Rohit', 'Sneha', 'Arjun', 'Pooja',
               'Vikram', 'Kavya', 'Amit', 'Neha', 'Siddharth', 'Riya', 'Akash',
               'Divya', 'Kiran', 'Simran', 'Rajesh', 'Meera', 'Vishal', 'Anjali',
               'Suresh', 'Deepika', 'Manish', 'Nisha', 'Arun', 'Pallavi']

LAST_NAMES = ['Sharma', 'Patel', 'Singh', 'Kumar', 'Reddy', 'Joshi', 'Gupta', 'Mehta',
              'Nair', 'Iyer', 'Rao', 'Verma', 'Agarwal', 'Mishra', 'Tiwari',
              'Chatterjee', 'Banerjee', 'Pillai', 'Sinha', 'Pandey']

SCHOOL_NAMES = [
    'IIT Delhi', 'IIT Bombay', 'BITS Pilani', 'NIT Trichy', 'VIT Vellore',
    'Manipal Institute of Technology', 'Amity University', 'SRM University',
    'Delhi University', 'Mumbai University', 'Bangalore University', 'Pune University',
    'JNTU Hyderabad', 'Anna University', 'Jadavpur University', 'Osmania University',
    'Calcutta University', 'Rajasthan University', 'Gujarat University', 'CSJMU Kanpur',
]

SCHOLARSHIP_PROVIDERS = [
    'Government of India', 'Ministry of Education', 'AICTE', 'UGC', 'State Government',
    'Tata Trusts', 'Infosys Foundation', 'Mahindra Pride', 'Reliance Foundation',
    'HDFC Credila', 'Wipro Cares', 'L&T Build India', 'ONGC Scholarship',
    'CRY Foundation', 'Akanksha Foundation', 'Teach For India', 'NSP Portal',
    'Sitaram Jindal Foundation', 'Vidyasaarathi', 'Buddy4Study', 'KVPY'
]


def seed_demo_accounts():
    """Create 5 demo accounts."""
    demos = [
        {'email': 'student@demo.com', 'role': 'student', 'first_name': 'Arjun', 'last_name': 'Sharma'},
        {'email': 'parent@demo.com', 'role': 'parent', 'first_name': 'Ramesh', 'last_name': 'Sharma'},
        {'email': 'school@demo.com', 'role': 'school', 'first_name': 'Admin', 'last_name': 'IIT Delhi'},
        {'email': 'donor@demo.com', 'role': 'donor', 'first_name': 'Sunita', 'last_name': 'Kapoor'},
        {'email': 'admin@demo.com', 'role': 'admin', 'first_name': 'Super', 'last_name': 'Admin'},
    ]

    for demo in demos:
        if not User.query.filter_by(email=demo['email']).first():
            pw = bcrypt.generate_password_hash('Demo@123').decode('utf-8')
            user = User(
                email=demo['email'],
                password_hash=pw,
                role=demo['role'],
                first_name=demo['first_name'],
                last_name=demo['last_name'],
                is_active=True,
                is_verified=True,
            )
            db.session.add(user)
            db.session.flush()

            if demo['role'] == 'student':
                student = Student(
                    user_id=user.id,
                    student_id='STU000001',
                    gender='Male',
                    category='General',
                    state='Maharashtra',
                    city='Mumbai',
                    degree='B.Tech',
                    branch='Computer Science',
                    year_of_study=2,
                    institution_name='IIT Bombay',
                    cgpa=8.4,
                    percentage=84,
                    annual_income=250000,
                    family_size=4,
                    disability_status=False,
                    achievements='State Rank 5 in JEE, Hackathon Winner',
                    skills='Python, Machine Learning, React',
                    extracurricular='Cricket, Robotics Club',
                    interests='AI, Data Science',
                    financial_health_score=68,
                    dropout_risk=0.12,
                    profile_completion=90,
                    attendance_percentage=85,
                    fee_due=15000,
                    scholarship_amount_received=50000,
                )
                db.session.add(student)

            elif demo['role'] == 'parent':
                parent = Parent(user_id=user.id, annual_income=250000, occupation='Teacher')
                db.session.add(parent)

            elif demo['role'] == 'school':
                school = School(
                    user_id=user.id,
                    name='IIT Bombay',
                    code='IITB001',
                    type='University',
                    affiliation='MHRD',
                    state='Maharashtra',
                    city='Mumbai',
                    total_students=12000,
                    scholarship_budget=5000000,
                    is_verified=True,
                )
                db.session.add(school)

            elif demo['role'] == 'donor':
                donor = Donor(
                    user_id=user.id,
                    type='individual',
                    organization_name='Kapoor Charitable Trust',
                    total_donated=500000,
                    students_supported=45,
                    is_verified=True,
                )
                db.session.add(donor)

    db.session.commit()
    print('✅ Demo accounts created')


def seed_scholarships():
    """Generate 200 scholarships."""
    scholarship_data = [
        # Government Scholarships
        {'name': 'NSP Post-Matric Scholarship for SC Students', 'type': 'government', 'provider': 'Government of India',
         'amount': 50000, 'max_income': 250000, 'eligible_categories': ['SC'], 'min_cgpa': 5.0,
         'description': 'Post-matric scholarship for SC students pursuing higher education.'},
        {'name': 'NSP Post-Matric Scholarship for ST Students', 'type': 'government', 'provider': 'Government of India',
         'amount': 50000, 'max_income': 250000, 'eligible_categories': ['ST'], 'min_cgpa': 5.0,
         'description': 'Post-matric scholarship for ST students across India.'},
        {'name': 'NSP Post-Matric Scholarship for OBC Students', 'type': 'government', 'provider': 'Government of India',
         'amount': 30000, 'max_income': 150000, 'eligible_categories': ['OBC'], 'min_cgpa': 5.0,
         'description': 'Financial support for OBC students in higher education.'},
        {'name': 'Central Sector Scheme of Scholarships', 'type': 'government', 'provider': 'Ministry of Education',
         'amount': 20000, 'max_income': 800000, 'eligible_categories': ['General', 'OBC', 'EWS'],
         'min_cgpa': 7.5, 'description': 'Merit-based scholarship for Class 12 toppers.'},
        {'name': 'Prime Minister\'s Special Scholarship Scheme', 'type': 'government', 'provider': 'Government of India',
         'amount': 30000, 'max_income': 600000, 'eligible_categories': ['General', 'OBC', 'SC', 'ST'],
         'description': 'For students from J&K pursuing higher education elsewhere.'},
        {'name': 'AICTE Pragati Scholarship for Girls', 'type': 'government', 'provider': 'AICTE',
         'amount': 50000, 'max_income': 800000, 'eligible_genders': ['Female'], 'min_cgpa': 6.0,
         'eligible_degrees': ['B.Tech', 'B.E.', 'Diploma'],
         'description': 'Scholarship for girl students in technical education.'},
        {'name': 'AICTE Saksham Scholarship', 'type': 'government', 'provider': 'AICTE',
         'amount': 50000, 'max_income': 800000, 'disability_only': True,
         'eligible_degrees': ['B.Tech', 'B.E.', 'Diploma'],
         'description': 'For differently-abled students in technical courses.'},
        {'name': 'UGC PG Scholarship for SC/ST', 'type': 'government', 'provider': 'UGC',
         'amount': 25000, 'eligible_categories': ['SC', 'ST'], 'eligible_degrees': ['M.Tech', 'M.Sc', 'MBA'],
         'description': 'Post-graduate scholarship for SC/ST students.'},
        {'name': 'ONGC Scholarship', 'type': 'government', 'provider': 'ONGC',
         'amount': 48000, 'max_income': 200000, 'min_percentage': 60,
         'eligible_degrees': ['B.Tech', 'B.E.', 'MBBS'],
         'description': 'ONGC scholarship for meritorious students.'},
        {'name': 'NTPC Scholarship', 'type': 'government', 'provider': 'NTPC',
         'amount': 36000, 'max_income': 300000, 'min_cgpa': 6.5,
         'eligible_degrees': ['B.Tech', 'B.E.'],
         'description': 'NTPC scholarship for engineering students.'},

        # AICTE / Technical
        {'name': 'AICTE-NDF Scholarship', 'type': 'government', 'provider': 'AICTE',
         'amount': 60000, 'max_income': 250000, 'min_cgpa': 6.0,
         'eligible_degrees': ['B.Tech', 'B.E.', 'M.Tech'],
         'description': 'National Development Fellowship for technical students.'},
        {'name': 'GATE Research Scholarship', 'type': 'government', 'provider': 'IITs/NITs',
         'amount': 312000, 'max_income': None, 'min_cgpa': 8.0,
         'eligible_degrees': ['M.Tech'],
         'description': 'Stipend for GATE qualified M.Tech students at IITs and NITs.'},

        # State Government
        {'name': 'Maharashtra State Government Scholarship', 'type': 'government', 'provider': 'Maharashtra Government',
         'amount': 25000, 'max_income': 150000, 'eligible_states': ['Maharashtra'],
         'description': 'State-level scholarship for financially weaker students in Maharashtra.'},
        {'name': 'Karnataka Rajyotsava Scholarship', 'type': 'government', 'provider': 'Karnataka Government',
         'amount': 20000, 'max_income': 200000, 'eligible_states': ['Karnataka'],
         'description': 'Government of Karnataka scholarship for higher education.'},
        {'name': 'UP Chief Minister Scholarship', 'type': 'government', 'provider': 'Uttar Pradesh Government',
         'amount': 18000, 'max_income': 200000, 'eligible_states': ['Uttar Pradesh'],
         'description': 'Uttar Pradesh state scholarship for meritorious students.'},
        {'name': 'Tamil Nadu Government Scholarship', 'type': 'government', 'provider': 'Tamil Nadu Government',
         'amount': 24000, 'max_income': 250000, 'eligible_states': ['Tamil Nadu'],
         'description': 'Financial aid for TN students in higher education.'},
        {'name': 'Rajasthan Chief Minister Scholarship', 'type': 'government', 'provider': 'Rajasthan Government',
         'amount': 15000, 'max_income': 150000, 'eligible_states': ['Rajasthan'],
         'description': 'Rajasthan state government scholarship.'},

        # CSR / Corporate
        {'name': 'Tata Scholarship', 'type': 'csr', 'provider': 'Tata Trusts',
         'amount': 100000, 'max_income': 400000, 'min_cgpa': 7.0,
         'description': 'Tata Trusts scholarship for underprivileged meritorious students at IITs and NITs.'},
        {'name': 'Infosys Foundation Scholarship', 'type': 'csr', 'provider': 'Infosys Foundation',
         'amount': 75000, 'max_income': 350000, 'min_cgpa': 7.5,
         'eligible_degrees': ['B.Tech', 'B.E.', 'M.Sc'],
         'description': 'Supporting tech-oriented students with financial assistance.'},
        {'name': 'Mahindra All India Talent Scholarship', 'type': 'csr', 'provider': 'Mahindra Pride',
         'amount': 80000, 'max_income': 250000, 'min_percentage': 70,
         'eligible_degrees': ['Diploma'],
         'description': 'Mahindra scholarship for diploma engineering students.'},
        {'name': 'Reliance Foundation Scholarship', 'type': 'csr', 'provider': 'Reliance Foundation',
         'amount': 200000, 'max_income': 250000, 'min_cgpa': 7.0,
         'eligible_degrees': ['B.Tech', 'B.E.', 'M.Sc', 'MBA'],
         'description': 'Reliance Foundation UG and PG scholarship.'},
        {'name': 'Wipro Cares Scholarship', 'type': 'csr', 'provider': 'Wipro Cares',
         'amount': 50000, 'max_income': 300000, 'min_cgpa': 7.0,
         'eligible_degrees': ['B.Tech', 'B.E.', 'B.Sc'],
         'description': 'Wipro scholarship for meritorious students in need.'},
        {'name': 'L&T Build India Scholarship', 'type': 'csr', 'provider': 'L&T',
         'amount': 60000, 'max_income': 250000, 'min_percentage': 65,
         'eligible_degrees': ['B.Tech', 'B.E.'],
         'description': 'L&T scholarship for engineering students.'},
        {'name': 'Hero MotoCorp Scholarship', 'type': 'csr', 'provider': 'Hero MotoCorp',
         'amount': 40000, 'max_income': 200000, 'min_cgpa': 6.5,
         'eligible_degrees': ['Diploma', 'B.Tech'],
         'description': 'Hero MotoCorp scholarship for technical education.'},
        {'name': 'Bajaj Scholarship', 'type': 'csr', 'provider': 'Bajaj Auto',
         'amount': 35000, 'max_income': 250000, 'min_cgpa': 7.0,
         'eligible_degrees': ['B.Tech', 'B.E.', 'Diploma'],
         'description': 'Bajaj scholarship supporting engineering students.'},
        {'name': 'HDFC Badhte Kadam Scholarship', 'type': 'csr', 'provider': 'HDFC Bank',
         'amount': 75000, 'max_income': 250000, 'min_percentage': 55,
         'eligible_degrees': ['B.Tech', 'B.A.', 'B.Sc', 'B.Com'],
         'description': 'HDFC Bank scholarship for class 10-graduation students.'},
        {'name': 'Axis Bank Foundation Scholarship', 'type': 'csr', 'provider': 'Axis Bank',
         'amount': 50000, 'max_income': 300000, 'min_percentage': 60,
         'description': 'Axis Bank scholarship for meritorious students.'},
        {'name': 'ICICI Foundation Scholarship', 'type': 'csr', 'provider': 'ICICI Foundation',
         'amount': 40000, 'max_income': 200000, 'min_cgpa': 6.5,
         'description': 'ICICI Foundation support for higher education.'},
        {'name': 'Kotak Kanya Scholarship', 'type': 'csr', 'provider': 'Kotak Education Foundation',
         'amount': 150000, 'max_income': 300000, 'eligible_genders': ['Female'],
         'eligible_degrees': ['B.Tech', 'B.E.', 'B.Sc', 'B.Com', 'B.A.'],
         'description': 'Scholarship exclusively for girl students from lower-income families.'},

        # NGO Scholarships
        {'name': 'Sitaram Jindal Foundation Scholarship', 'type': 'ngo', 'provider': 'Sitaram Jindal Foundation',
         'amount': 36000, 'max_income': 250000, 'min_percentage': 60,
         'description': 'Jindal Foundation scholarship for needy students across India.'},
        {'name': 'Swami Vivekananda Scholarship', 'type': 'ngo', 'provider': 'West Bengal Government/NGO',
         'amount': 120000, 'max_income': 250000, 'min_cgpa': 7.0,
         'eligible_states': ['West Bengal'],
         'description': 'Premier scholarship for WB students pursuing higher education.'},
        {'name': 'Narotam Sekhsaria Foundation', 'type': 'ngo', 'provider': 'NSS Foundation',
         'amount': 250000, 'max_income': 500000, 'min_cgpa': 7.5,
         'eligible_degrees': ['B.Tech', 'MBBS', 'MBA', 'M.Sc'],
         'description': 'NSS Foundation scholarship for college and PG students.'},
        {'name': 'Jamnalal Bajaj Foundation Scholarship', 'type': 'ngo', 'provider': 'Jamnalal Bajaj Foundation',
         'amount': 180000, 'max_income': 400000, 'min_cgpa': 7.5,
         'description': 'Bajaj Foundation scholarship for science and management students.'},
        {'name': 'BMS Scholarship', 'type': 'ngo', 'provider': 'Bharatiya Mazdoor Sangh',
         'amount': 15000, 'max_income': 150000,
         'description': 'BMS scholarship supporting workers\' children.'},
        {'name': 'Motilal Oswal Foundation Scholarship', 'type': 'ngo', 'provider': 'Motilal Oswal Foundation',
         'amount': 100000, 'max_income': 400000, 'min_cgpa': 7.0,
         'eligible_degrees': ['B.Com', 'BBA', 'MBA'],
         'description': 'Scholarship for finance and management students.'},

        # Alumni
        {'name': 'IIT Alumni Scholarship', 'type': 'alumni', 'provider': 'IIT Alumni Association',
         'amount': 200000, 'max_income': 300000, 'min_cgpa': 8.0,
         'eligible_degrees': ['B.Tech', 'M.Tech'],
         'description': 'Alumni-funded scholarship for current IIT students in financial need.'},
        {'name': 'NIT Alumni Scholarship', 'type': 'alumni', 'provider': 'NIT Alumni Network',
         'amount': 100000, 'max_income': 300000, 'min_cgpa': 7.5,
         'eligible_degrees': ['B.Tech', 'M.Tech'],
         'description': 'NIT alumni scholarship for deserving students.'},

        # Emergency / Crowdfunding
        {'name': 'EduBridge Emergency Fund', 'type': 'emergency', 'provider': 'EduBridge AI Platform',
         'amount': 25000, 'max_income': 200000,
         'description': 'Emergency educational assistance for students facing financial crisis.'},
        {'name': 'CrowdFund My Education', 'type': 'crowdfunding', 'provider': 'Milaap/Ketto',
         'amount': 50000, 'max_income': 300000,
         'description': 'Crowdfunding support for education via Milaap or Ketto platforms.'},
    ]

    # Add more auto-generated scholarships to reach 200
    extra_scholarships = []
    for i in range(160):
        s_type = random.choice(['government', 'csr', 'ngo', 'alumni', 'crowdfunding', 'emergency'])
        provider = random.choice(SCHOLARSHIP_PROVIDERS)
        state = random.choice(STATES + ['All India'])
        degree = random.choice(DEGREES)
        category = random.choice(CATEGORIES + ['All'])
        gender = random.choice(['All', 'All', 'All', 'Male', 'Female'])
        amount = random.choice([10000, 15000, 20000, 25000, 30000, 40000, 50000, 60000, 75000, 100000])
        max_income = random.choice([100000, 150000, 200000, 250000, 300000, 400000, 500000, None])
        min_cgpa = random.choice([0, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5, 8.0])

        extra_scholarships.append({
            'name': f'{provider} Scholarship {i + 1} for {degree}',
            'type': s_type,
            'provider': provider,
            'amount': amount,
            'max_income': max_income,
            'eligible_states': [state] if state != 'All India' else [],
            'eligible_degrees': [degree],
            'eligible_categories': [category] if category != 'All' else [],
            'eligible_genders': [gender] if gender != 'All' else [],
            'min_cgpa': min_cgpa,
            'description': f'Scholarship by {provider} for {degree} students' + (f' in {state}' if state != 'All India' else ''),
        })

    all_scholarships = scholarship_data + extra_scholarships

    count = 0
    for s_data in all_scholarships:
        if Scholarship.query.filter_by(name=s_data['name']).first():
            continue

        deadline = date.today() + timedelta(days=random.randint(30, 365))
        docs_required = random.sample([
            'Income Certificate', 'Marksheet', 'Aadhaar Card', 'Bank Passbook',
            'Bonafide Certificate', 'Caste Certificate', 'Disability Certificate',
            'Passport Photo', 'Institution Fee Receipt'
        ], k=random.randint(3, 6))

        s = Scholarship(
            name=s_data['name'],
            provider=s_data.get('provider', 'Unknown'),
            type=s_data.get('type', 'government'),
            description=s_data.get('description', ''),
            amount=s_data.get('amount'),
            min_amount=s_data.get('amount', 10000) * 0.5,
            max_amount=s_data.get('amount', 10000) * 1.5,
            max_income=s_data.get('max_income'),
            min_cgpa=s_data.get('min_cgpa', 0),
            min_percentage=s_data.get('min_percentage', 0),
            eligible_degrees=json.dumps(s_data.get('eligible_degrees', [])),
            eligible_states=json.dumps(s_data.get('eligible_states', [])),
            eligible_categories=json.dumps(s_data.get('eligible_categories', [])),
            eligible_genders=json.dumps(s_data.get('eligible_genders', [])),
            disability_only=s_data.get('disability_only', False),
            documents_required=json.dumps(docs_required),
            tags=json.dumps(random.sample(['merit', 'need-based', 'technical', 'girls', 'minority', 'SC/ST', 'disability'], k=2)),
            deadline=deadline,
            total_seats=random.randint(10, 500),
            filled_seats=random.randint(0, 50),
            renewal_possible=random.choice([True, False]),
        )
        db.session.add(s)
        count += 1
        if count % 50 == 0:
            db.session.commit()

    db.session.commit()
    print(f'✅ {count} scholarships created')


def seed_students():
    """Generate 100 students."""
    count = 0
    for i in range(100):
        email = f'student{i+1}@edubridge.demo'
        if User.query.filter_by(email=email).first():
            continue

        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        pw = bcrypt.generate_password_hash('Demo@123').decode('utf-8')

        user = User(email=email, password_hash=pw, role='student',
                    first_name=first, last_name=last,
                    is_active=True, is_verified=True)
        db.session.add(user)
        db.session.flush()

        income = random.randint(50000, 600000)
        cgpa = round(random.uniform(5.0, 9.5), 1)
        attendance = round(random.uniform(55, 98), 1)
        fee_due = random.choice([0, 0, 0, 5000, 10000, 20000, 50000, 100000])

        student = Student(
            user_id=user.id,
            student_id=f'STU{100 + i:06d}',
            gender=random.choice(GENDERS),
            category=random.choice(CATEGORIES),
            state=random.choice(STATES),
            city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata']),
            degree=random.choice(DEGREES),
            branch=random.choice(BRANCHES),
            year_of_study=random.randint(1, 4),
            institution_name=random.choice(SCHOOL_NAMES),
            cgpa=cgpa,
            percentage=round(cgpa * 9.5, 1),
            annual_income=income,
            family_size=random.randint(2, 8),
            disability_status=random.random() < 0.05,
            achievements=random.choice(['State rank holder', 'Hackathon winner', 'NSS volunteer', 'Sports captain', '']),
            skills=random.choice(['Python, Java', 'C++, MATLAB', 'Excel, PowerBI', 'CAD, ANSYS', '']),
            extracurricular=random.choice(['Cricket', 'Music', 'Debate', 'Dance', 'Robotics', '']),
            interests=random.choice(['AI/ML', 'Finance', 'Research', 'Entrepreneurship', '']),
            financial_health_score=round(random.uniform(30, 90), 1),
            dropout_risk=round(random.uniform(0.05, 0.60), 3),
            profile_completion=random.randint(40, 100),
            attendance_percentage=attendance,
            fee_due=fee_due,
            scholarship_amount_received=random.choice([0, 0, 10000, 25000, 50000]),
        )
        db.session.add(student)
        count += 1

        if count % 20 == 0:
            db.session.commit()

    db.session.commit()
    print(f'✅ {count} students created')


def seed_schools():
    """Generate 20 schools."""
    count = 0
    for i, school_name in enumerate(SCHOOL_NAMES):
        email = f'school{i+1}@edubridge.demo'
        if User.query.filter_by(email=email).first():
            continue

        pw = bcrypt.generate_password_hash('Demo@123').decode('utf-8')
        user = User(email=email, password_hash=pw, role='school',
                    first_name='Admin', last_name=school_name,
                    is_active=True, is_verified=True)
        db.session.add(user)
        db.session.flush()

        school = School(
            user_id=user.id,
            name=school_name,
            code=f'SCH{i+1:04d}',
            type=random.choice(['University', 'College', 'Institute']),
            affiliation=random.choice(['UGC', 'AICTE', 'MCI', 'State Board']),
            state=random.choice(STATES),
            city=random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune']),
            total_students=random.randint(1000, 20000),
            scholarship_budget=random.randint(500000, 10000000),
            is_verified=True,
        )
        db.session.add(school)
        count += 1

    db.session.commit()
    print(f'✅ {count} schools created')


def seed_donors():
    """Generate 20 donors."""
    ngo_names = ['Akanksha Foundation', 'CRY', 'Teach For India', 'Pratham', 'Magic Bus',
                 'Dream A Dream', 'iTeach Schools', 'Gyan Shala', 'Samhita', 'Aser Centre',
                 'Udaan India', 'Literacy India', 'Shiksha Foundation', 'Nanhi Kali', 'EdTech NGO']
    count = 0
    for i in range(20):
        email = f'donor{i+1}@edubridge.demo'
        if User.query.filter_by(email=email).first():
            continue

        pw = bcrypt.generate_password_hash('Demo@123').decode('utf-8')
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        d_type = random.choice(['individual', 'ngo', 'csr', 'alumni'])

        user = User(email=email, password_hash=pw, role='donor',
                    first_name=first, last_name=last,
                    is_active=True, is_verified=True)
        db.session.add(user)
        db.session.flush()

        total_donated = random.randint(10000, 5000000)
        donor = Donor(
            user_id=user.id,
            type=d_type,
            organization_name=random.choice(ngo_names) if d_type in ['ngo', 'csr'] else f'{first} {last} Foundation',
            total_donated=total_donated,
            students_supported=random.randint(1, 100),
            is_verified=True,
        )
        db.session.add(donor)
        count += 1

    db.session.commit()
    print(f'✅ {count} donors created')


def seed_applications():
    """Generate ~100 applications."""
    students = Student.query.limit(50).all()
    scholarships = Scholarship.query.limit(30).all()
    statuses = ['submitted', 'submitted', 'under_review', 'approved', 'rejected', 'disbursed']

    count = 0
    for student in students:
        n_apps = random.randint(1, 4)
        picked = random.sample(scholarships, min(n_apps, len(scholarships)))
        for sch in picked:
            if Application.query.filter_by(student_id=student.id, scholarship_id=sch.id).first():
                continue
            fit_score = round(random.uniform(30, 95), 1)
            status = random.choice(statuses)
            app = Application(
                student_id=student.id,
                scholarship_id=sch.id,
                status=status,
                fit_score=fit_score,
                selection_probability=fit_score / 100 * 0.8,
                submitted_at=datetime.utcnow() - timedelta(days=random.randint(1, 90)),
                amount_approved=sch.amount if status in ['approved', 'disbursed'] else None,
            )
            db.session.add(app)
            count += 1

    db.session.commit()
    print(f'✅ {count} applications created')


def seed_donations():
    """Generate 50 donations."""
    donors = Donor.query.limit(20).all()
    students = Student.query.limit(30).all()
    count = 0
    import uuid

    for donor in donors:
        n_donations = random.randint(1, 5)
        for _ in range(n_donations):
            student = random.choice(students) if students else None
            amount = random.choice([5000, 10000, 25000, 50000, 100000, 200000])
            donation = Donation(
                donor_id=donor.id,
                student_id=student.id if student else None,
                amount=amount,
                purpose=random.choice(['Tuition Fee', 'Books & Materials', 'Hostel Fee', 'General Support']),
                status='completed',
                transaction_id=str(uuid.uuid4())[:12].upper(),
                donated_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            )
            db.session.add(donation)
            count += 1

    db.session.commit()
    print(f'✅ {count} donations created')


def seed_notifications():
    """Add sample notifications for demo student."""
    demo_user = User.query.filter_by(email='student@demo.com').first()
    if not demo_user:
        return

    msgs = [
        ('New Scholarship Available', 'NSP Post-Matric Scholarship is now accepting applications. Deadline: Oct 31', 'scholarship'),
        ('Application Status Update', 'Your application for AICTE Pragati Scholarship has been approved! ₹50,000 will be disbursed.', 'application'),
        ('Document Verified', 'Your Income Certificate has been successfully verified.', 'system'),
        ('Deadline Reminder', 'Tata Scholarship deadline is in 7 days. Complete your application now!', 'scholarship'),
        ('Financial Health Alert', 'Your Financial Health Score has improved to 72. Keep it up!', 'alert'),
        ('New Message', 'Your school has reviewed your scholarship request.', 'system'),
        ('Payment Received', '₹25,000 has been credited to your account from ONGC Scholarship.', 'payment'),
    ]

    for title, message, n_type in msgs:
        if not Notification.query.filter_by(user_id=demo_user.id, title=title).first():
            n = Notification(
                user_id=demo_user.id,
                title=title,
                message=message,
                type=n_type,
                is_read=random.choice([True, False]),
            )
            db.session.add(n)

    db.session.commit()
    print('✅ Sample notifications created')


if __name__ == '__main__':
    with app.app_context():
        print('🚀 Starting EduBridge AI database seed...')
        db.create_all()
        seed_demo_accounts()
        seed_scholarships()
        seed_students()
        seed_schools()
        seed_donors()
        seed_applications()
        seed_donations()
        seed_notifications()
        print('\n✅ Database seeded successfully!')
        print('\n📋 Demo Accounts:')
        print('  Student: student@demo.com / Demo@123')
        print('  Parent:  parent@demo.com  / Demo@123')
        print('  School:  school@demo.com  / Demo@123')
        print('  Donor:   donor@demo.com   / Demo@123')
        print('  Admin:   admin@demo.com   / Demo@123')
