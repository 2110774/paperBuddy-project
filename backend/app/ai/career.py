# AI Career Guidance Engine
# Suggests careers, courses, internships based on student profile


CAREER_PATHS = {
    'computer science': {
        'careers': ['Software Engineer', 'Data Scientist', 'ML Engineer', 'Cybersecurity Analyst', 'Cloud Architect', 'Product Manager'],
        'courses': ['Full Stack Development (Coursera)', 'Machine Learning Specialization (Andrew Ng)', 'AWS Cloud Practitioner', 'Google Data Analytics Certificate'],
        'internships': ['Google STEP Intern', 'Microsoft Explore', 'Amazon SDE Intern', 'Infosys InStep', 'TCS iBegin'],
        'skills': ['Python', 'DSA', 'System Design', 'SQL', 'Cloud Computing'],
        'avg_salary': '₹8–35 LPA',
    },
    'electronics': {
        'careers': ['VLSI Engineer', 'Embedded Systems Developer', 'IoT Engineer', 'RF Engineer', 'PCB Designer'],
        'courses': ['VLSI Design (NPTEL)', 'Embedded C Programming', 'ARM Cortex Programming', 'IoT with Raspberry Pi'],
        'internships': ['ISRO Internship', 'DRDO Internship', 'Qualcomm Intern', 'Texas Instruments Intern'],
        'skills': ['VHDL', 'Verilog', 'C/C++', 'MATLAB', 'PCB Design'],
        'avg_salary': '₹5–20 LPA',
    },
    'mechanical': {
        'careers': ['Design Engineer', 'Manufacturing Engineer', 'Aerospace Engineer', 'Automotive Engineer', 'R&D Engineer'],
        'courses': ['CAD/CAM with SolidWorks', 'Finite Element Analysis', 'Six Sigma Green Belt', 'AutoCAD Certification'],
        'internships': ['Tata Motors Intern', 'Mahindra Intern', 'L&T Intern', 'BHEL Intern', 'HAL Trainee'],
        'skills': ['CAD', 'SolidWorks', 'ANSYS', 'GD&T', 'Thermodynamics'],
        'avg_salary': '₹4–18 LPA',
    },
    'civil': {
        'careers': ['Structural Engineer', 'Urban Planner', 'Geotechnical Engineer', 'Construction Manager', 'Environmental Engineer'],
        'courses': ['STAAD Pro Certification', 'AutoCAD Civil 3D', 'Project Management (PMP)', 'GIS & Remote Sensing'],
        'internships': ['L&T Construction Intern', 'NHAI Intern', 'PWD Internship', 'Gammon India Intern'],
        'skills': ['AutoCAD', 'STAAD Pro', 'Revit', 'MS Project', 'Structural Analysis'],
        'avg_salary': '₹4–15 LPA',
    },
    'business': {
        'careers': ['Business Analyst', 'Management Consultant', 'Financial Analyst', 'Marketing Manager', 'Entrepreneur'],
        'courses': ['CFA Level 1', 'Google Digital Marketing', 'Data Analytics for Business', 'MBA Entrance Prep (CAT/GMAT)'],
        'internships': ['McKinsey Business Analyst Intern', 'Deloitte Intern', 'Goldman Sachs Summer Analyst', 'Big4 Intern'],
        'skills': ['Excel', 'PowerBI', 'Financial Modeling', 'Communication', 'Leadership'],
        'avg_salary': '₹6–25 LPA',
    },
    'medicine': {
        'careers': ['Doctor (MBBS/MD)', 'Researcher', 'Healthcare Administrator', 'Medical Writer', 'Clinical Data Manager'],
        'courses': ['USMLE Prep', 'Medical Research Methodology', 'Clinical Trials Management', 'PG Medical Entrance Prep'],
        'internships': ['AIIMS Research Internship', 'Hospital Clinical Rotation', 'ICMR Research Project'],
        'skills': ['Clinical Skills', 'Research Methodology', 'Medical Writing', 'Statistics', 'Ethics'],
        'avg_salary': '₹8–50 LPA',
    },
    'default': {
        'careers': ['Research Analyst', 'Educator', 'Content Writer', 'Government Job (UPSC/SSC)', 'Entrepreneur'],
        'courses': ['Digital Marketing', 'Data Analytics', 'Communication Skills', 'Project Management'],
        'internships': ['NGO Internship', 'Government Internship Program', 'Startup Internship via LinkedIn'],
        'skills': ['Communication', 'Excel', 'Research', 'Problem Solving', 'Leadership'],
        'avg_salary': '₹3–15 LPA',
    }
}

SCHOLARSHIP_IMPACT = {
    'high_cgpa': {
        'careers': ['Research Scientist', 'Academic Faculty', 'GATE/CAT Topper Path', 'Foreign University Scholarship'],
        'courses': ['GRE Prep for MS/PhD', 'GATE Exam Preparation', 'Research Methodology'],
        'scholarships': ['DST-INSPIRE', 'CSIR-JRF', 'KVPY (for science students)', 'Kishore Vaigyanik Protsahan Yojana'],
    },
    'low_income': {
        'priority_scholarships': ['NSP Post-Matric', 'PM Scholarship', 'Minority Scholarship', 'State Government Scholarships'],
        'career_advice': 'Focus on government jobs and PSU careers for stability. Explore GATE for PSU recruitment.',
    }
}


def get_career_guidance(student_data: dict) -> dict:
    """
    Suggest careers, courses, internships based on student profile.
    """
    branch = (student_data.get('branch') or '').lower()
    cgpa = student_data.get('cgpa') or 0
    interests = (student_data.get('interests') or '').lower()
    skills = (student_data.get('skills') or '').lower()
    income = student_data.get('annual_income') or 0
    degree = (student_data.get('degree') or '').lower()

    # Match branch to career path
    matched_path = None
    for key in CAREER_PATHS:
        if key == 'default':
            continue
        if key in branch or key in interests or any(k in branch for k in key.split()):
            matched_path = CAREER_PATHS[key]
            break

    if not matched_path:
        if 'bcom' in branch or 'commerce' in branch or 'mba' in branch or 'bba' in branch:
            matched_path = CAREER_PATHS['business']
        elif 'medical' in branch or 'mbbs' in branch or 'pharma' in branch:
            matched_path = CAREER_PATHS['medicine']
        else:
            matched_path = CAREER_PATHS['default']

    careers = matched_path['careers'][:5]
    courses = matched_path['courses'][:4]
    internships = matched_path['internships'][:4]
    skills_to_develop = matched_path['skills'][:5]

    # High CGPA bonuses
    extra_notes = []
    if cgpa >= 8.5:
        extra_notes.append('🌟 Your CGPA qualifies you for research fellowships and top-tier internships.')
        extra_notes.append('Consider applying for DST-INSPIRE or CSIR-JRF research scholarships.')
        careers = ['Research Scientist', 'PhD/MS Abroad'] + careers[:3]
    elif cgpa >= 7.5:
        extra_notes.append('✅ Good CGPA — you qualify for most merit scholarships and reputed companies.')
    else:
        extra_notes.append('📈 Focus on improving CGPA to unlock more career opportunities and scholarships.')
        extra_notes.append('Consider skill certifications to complement your academic profile.')

    if income < 200000:
        extra_notes.append('💡 Given your income level, prioritize government jobs (UPSC/SSC/PSU) for stability.')

    confidence = 0.65 + (0.1 if cgpa >= 7 else 0) + (0.1 if branch else 0) + (0.05 if interests else 0)

    return {
        'careers': careers,
        'courses': courses,
        'internships': internships,
        'skills_to_develop': skills_to_develop,
        'avg_salary': matched_path.get('avg_salary', '₹4–15 LPA'),
        'extra_notes': extra_notes,
        'confidence_score': round(min(0.95, confidence), 2),
        'based_on': {
            'branch': branch or 'not specified',
            'cgpa': cgpa,
            'interests': interests or 'not specified',
        }
    }
