# AI Dropout Risk Prediction
# Rule-based + weighted scoring (XGBoost-style logic without model training requirement)


def predict_dropout_risk(student_data: dict) -> dict:
    """
    Predict financial and academic dropout risk.
    Returns probability (0-1), risk level, and recommendations.
    """
    cgpa = student_data.get('cgpa', 0) or 0
    attendance = student_data.get('attendance', 0) or 0
    annual_income = student_data.get('annual_income', 0) or 0
    fee_due = student_data.get('fee_due', 0) or 0
    year_of_study = student_data.get('year_of_study', 1) or 1
    family_size = student_data.get('family_size', 4) or 4

    # Weighted risk factors (higher = more risk)
    financial_risk = 0
    academic_risk = 0
    recommendations = []

    # Financial risk factors
    per_capita = annual_income / max(family_size, 1)
    if per_capita < 50000:
        financial_risk += 0.35
        recommendations.append('Apply for PM Scholarship, NSP, or state-level government scholarships.')
    elif per_capita < 150000:
        financial_risk += 0.20
        recommendations.append('Explore NGO and CSR scholarship opportunities.')
    elif per_capita < 300000:
        financial_risk += 0.10

    if fee_due > 50000:
        financial_risk += 0.30
        recommendations.append('Contact school for installment plan or emergency fund.')
    elif fee_due > 20000:
        financial_risk += 0.15
    elif fee_due > 5000:
        financial_risk += 0.05

    # Academic risk factors
    if cgpa < 5.0:
        academic_risk += 0.35
        recommendations.append('Seek academic counseling and tutoring support.')
    elif cgpa < 6.0:
        academic_risk += 0.20
        recommendations.append('Join study groups and improve attendance.')
    elif cgpa < 7.0:
        academic_risk += 0.10

    if attendance < 50:
        academic_risk += 0.35
        recommendations.append('Critical: Attendance below 50% risks academic dismissal.')
    elif attendance < 65:
        academic_risk += 0.25
        recommendations.append('Attendance below 75% threshold — improve immediately.')
    elif attendance < 75:
        academic_risk += 0.10

    # Year of study factor (first year most at risk)
    year_factor = max(0, 0.15 - (year_of_study - 1) * 0.04)
    financial_risk += year_factor

    # Combined dropout probability
    dropout_probability = (financial_risk * 0.6 + academic_risk * 0.4)
    dropout_probability = max(0.02, min(0.95, dropout_probability))

    # Risk level
    if dropout_probability >= 0.7:
        risk_level = 'critical'
    elif dropout_probability >= 0.5:
        risk_level = 'high'
    elif dropout_probability >= 0.3:
        risk_level = 'moderate'
    elif dropout_probability >= 0.15:
        risk_level = 'low'
    else:
        risk_level = 'minimal'

    # Default recommendations
    if not recommendations:
        recommendations = [
            'Maintain current attendance and CGPA.',
            'Explore scholarship renewals for continued support.',
        ]

    return {
        'dropout_probability': round(dropout_probability, 3),
        'risk_level': risk_level,
        'financial_risk': round(min(1.0, financial_risk), 3),
        'academic_risk': round(min(1.0, academic_risk), 3),
        'recommendations': recommendations[:4],
        'interpretation': _interpret_risk(dropout_probability),
        'factors': {
            'per_capita_income': round(per_capita),
            'cgpa': cgpa,
            'attendance': attendance,
            'fee_due': fee_due,
            'year_of_study': year_of_study,
        }
    }


def _interpret_risk(prob: float) -> str:
    if prob >= 0.7:
        return 'Critical risk: Immediate intervention required. Multiple high-risk factors detected.'
    elif prob >= 0.5:
        return 'High risk: Student may drop out without financial and academic support.'
    elif prob >= 0.3:
        return 'Moderate risk: Monitor closely and apply for available scholarships.'
    elif prob >= 0.15:
        return 'Low risk: Minor concerns. Maintain performance and explore funding options.'
    else:
        return 'Minimal risk: Student is financially and academically stable.'
