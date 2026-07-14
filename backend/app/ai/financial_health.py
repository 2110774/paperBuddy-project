# Financial Health Score Calculator
# No external APIs — pure Python calculations


def calculate_financial_health(student_data: dict) -> dict:
    """
    Generate a financial health score (0–100) for a student.
    
    Inputs:
        annual_income, cgpa, attendance, fee_due,
        scholarship_received, family_size
    """
    score = 0
    components = {}
    suggestions = []
    risk_level = 'low'

    income = student_data.get('annual_income', 0) or 0
    cgpa = student_data.get('cgpa', 0) or 0
    attendance = student_data.get('attendance', 0) or 0
    fee_due = student_data.get('fee_due', 0) or 0
    scholarship_received = student_data.get('scholarship_received', 0) or 0
    family_size = student_data.get('family_size', 4) or 4

    # 1. Income Score (25 points)
    # Per capita income benchmark: ₹1.5L = poor, ₹3L = middle, ₹6L+ = comfortable
    per_capita = income / max(family_size, 1)
    if per_capita >= 600000:
        income_score = 25
    elif per_capita >= 300000:
        income_score = 18
    elif per_capita >= 150000:
        income_score = 10
    elif per_capita >= 60000:
        income_score = 5
    else:
        income_score = 2
        suggestions.append('Apply for low-income government scholarships immediately.')
    components['income_score'] = income_score
    score += income_score

    # 2. Academic Performance Score (25 points)
    if cgpa >= 9.0:
        acad_score = 25
    elif cgpa >= 8.0:
        acad_score = 20
    elif cgpa >= 7.0:
        acad_score = 15
    elif cgpa >= 6.0:
        acad_score = 10
    elif cgpa >= 5.0:
        acad_score = 5
    else:
        acad_score = 2
        suggestions.append('Focus on improving academic performance to qualify for merit scholarships.')
    components['academic_score'] = acad_score
    score += acad_score

    # 3. Attendance Score (20 points)
    if attendance >= 90:
        att_score = 20
    elif attendance >= 75:
        att_score = 15
    elif attendance >= 60:
        att_score = 8
    else:
        att_score = 2
        suggestions.append('Low attendance risks scholarship eligibility. Improve attendance.')
    components['attendance_score'] = att_score
    score += att_score

    # 4. Fee Clearance Score (20 points)
    if fee_due <= 0:
        fee_score = 20
    elif fee_due <= 10000:
        fee_score = 15
        suggestions.append('Clear pending fee dues to avoid academic issues.')
    elif fee_due <= 50000:
        fee_score = 8
        suggestions.append('Significant fee dues — apply for emergency funds or installment plan.')
    else:
        fee_score = 2
        suggestions.append('Critical: High fee dues. Apply for NGO emergency funding immediately.')
    components['fee_clearance_score'] = fee_score
    score += fee_score

    # 5. Scholarship Coverage Score (10 points)
    if scholarship_received >= income * 0.5:
        sch_score = 10
        suggestions.append('Good scholarship coverage. Explore renewal opportunities.')
    elif scholarship_received > 0:
        sch_score = 6
    else:
        sch_score = 0
        suggestions.append('No scholarship received. Apply via EduBridge AI recommendations.')
    components['scholarship_score'] = sch_score
    score += sch_score

    score = max(0, min(100, score))

    # Risk level
    if score >= 75:
        risk_level = 'low'
    elif score >= 50:
        risk_level = 'medium'
    elif score >= 30:
        risk_level = 'high'
    else:
        risk_level = 'critical'

    # Default suggestions if none
    if not suggestions:
        suggestions.append('Maintain current academic performance and income stability.')
        suggestions.append('Explore merit scholarships for top-performing students.')

    confidence = min(0.95, 0.6 + (len([v for v in student_data.values() if v]) / len(student_data)) * 0.35)

    return {
        'score': round(score, 1),
        'risk_level': risk_level,
        'components': components,
        'suggestions': suggestions[:4],
        'confidence': round(confidence, 2),
        'interpretation': _interpret_score(score),
        'per_capita_income': round(per_capita),
    }


def _interpret_score(score: float) -> str:
    if score >= 80:
        return 'Excellent financial health. You have strong stability and good scholarship prospects.'
    elif score >= 65:
        return 'Good financial standing. A few improvements could open up more funding opportunities.'
    elif score >= 50:
        return 'Moderate financial risk. Consider applying for scholarships and fee assistance.'
    elif score >= 35:
        return 'High financial risk. Immediate action recommended — apply for emergency funds.'
    else:
        return 'Critical financial situation. Contact school financial aid office immediately.'
