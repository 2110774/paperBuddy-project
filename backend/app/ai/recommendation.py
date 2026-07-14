# AI Scholarship Recommendation Engine
# Uses rule-based scoring + cosine similarity (no external LLM APIs)

from app.models import Scholarship
import json
import math
from datetime import date


def calculate_fit_score(student_data: dict, scholarship: dict) -> dict:
    """
    Calculate how well a student fits a scholarship.
    Returns score (0-100) and probability.
    """
    score = 0
    max_score = 100
    reasons = []
    disqualifiers = []

    # 1. Income check (25 points)
    income = student_data.get('annual_income', 0) or 0
    max_income = scholarship.get('max_income')
    if max_income:
        if income <= max_income:
            income_ratio = 1 - (income / max_income)
            points = min(25, int(income_ratio * 30))
            score += points
            reasons.append(f'Income ₹{income:,.0f} is within limit of ₹{max_income:,.0f}')
        else:
            disqualifiers.append(f'Income ₹{income:,.0f} exceeds limit of ₹{max_income:,.0f}')
            return {
                'score': 0,
                'probability': 0.02,
                'eligible': False,
                'reasons': reasons,
                'disqualifiers': disqualifiers,
            }
    else:
        score += 15  # No income requirement
        reasons.append('No income restriction')

    # 2. CGPA / Percentage (20 points)
    cgpa = student_data.get('cgpa', 0) or 0
    percentage = student_data.get('percentage', 0) or 0
    min_cgpa = scholarship.get('min_cgpa', 0) or 0
    min_pct = scholarship.get('min_percentage', 0) or 0

    if min_cgpa > 0 and cgpa > 0:
        if cgpa >= min_cgpa:
            excess = cgpa - min_cgpa
            points = min(20, int(10 + excess * 4))
            score += points
            reasons.append(f'CGPA {cgpa} meets minimum {min_cgpa}')
        else:
            disqualifiers.append(f'CGPA {cgpa} below minimum {min_cgpa}')
            score -= 15
    elif min_pct > 0 and percentage > 0:
        if percentage >= min_pct:
            score += 15
            reasons.append(f'Percentage {percentage}% meets minimum {min_pct}%')
        else:
            score -= 10
    else:
        score += 12
        reasons.append('No academic cutoff requirement')

    # 3. Category match (15 points)
    student_cat = (student_data.get('category') or '').upper()
    eligible_cats = [c.upper() for c in (scholarship.get('eligible_categories') or [])]
    if eligible_cats:
        if student_cat in eligible_cats or 'ALL' in eligible_cats:
            score += 15
            reasons.append(f'Category {student_cat} is eligible')
        else:
            disqualifiers.append(f'Category {student_cat} not in eligible list')
            return {
                'score': 10,
                'probability': 0.05,
                'eligible': False,
                'reasons': reasons,
                'disqualifiers': disqualifiers,
            }
    else:
        score += 10

    # 4. State match (10 points)
    student_state = (student_data.get('state') or '').lower()
    eligible_states = [s.lower() for s in (scholarship.get('eligible_states') or [])]
    if eligible_states:
        if student_state in eligible_states or 'all' in eligible_states or 'pan india' in eligible_states:
            score += 10
            reasons.append('State is eligible')
        else:
            score += 2
    else:
        score += 8  # National scholarship

    # 5. Degree match (10 points)
    student_degree = (student_data.get('degree') or '').lower()
    eligible_degrees = [d.lower() for d in (scholarship.get('eligible_degrees') or [])]
    if eligible_degrees:
        if student_degree in eligible_degrees or 'all' in eligible_degrees:
            score += 10
            reasons.append(f'Degree {student_degree} matches')
        elif any(deg in student_degree for deg in eligible_degrees):
            score += 6
        else:
            score += 1
    else:
        score += 8

    # 6. Gender (5 points)
    student_gender = (student_data.get('gender') or '').lower()
    eligible_genders = scholarship.get('eligible_genders') or []
    if isinstance(eligible_genders, str):
        try:
            eligible_genders = json.loads(eligible_genders)
        except Exception:
            eligible_genders = []
    eligible_genders_lower = [g.lower() for g in eligible_genders]
    if eligible_genders_lower:
        if student_gender in eligible_genders_lower or 'all' in eligible_genders_lower:
            score += 5
    else:
        score += 5

    # 7. Disability (5 points)
    disability_only = scholarship.get('disability_only', False)
    student_disability = student_data.get('disability_status', False)
    if disability_only:
        if student_disability:
            score += 10
            reasons.append('Disability-specific scholarship — you qualify')
        else:
            return {
                'score': 5,
                'probability': 0.01,
                'eligible': False,
                'reasons': [],
                'disqualifiers': ['This scholarship is for differently-abled students only'],
            }
    elif student_disability:
        score += 3

    # 8. Deadline bonus (5 points)
    deadline = scholarship.get('deadline')
    if deadline:
        try:
            if isinstance(deadline, str):
                deadline_date = date.fromisoformat(deadline)
            else:
                deadline_date = deadline
            days_left = (deadline_date - date.today()).days
            if days_left > 30:
                score += 5
            elif days_left > 7:
                score += 3
            elif days_left < 0:
                score = max(0, score - 20)
                disqualifiers.append('Deadline has passed')
        except Exception:
            pass

    score = max(0, min(100, score))
    probability = min(0.95, max(0.02, score / 100 * 0.85 + 0.05))

    eligible = len(disqualifiers) == 0 and score >= 30

    return {
        'score': round(score, 1),
        'probability': round(probability, 2),
        'eligible': eligible,
        'reasons': reasons,
        'disqualifiers': disqualifiers,
    }


def recommend_scholarships(student_data: dict, limit: int = 20) -> list:
    """
    Recommend top scholarships for a student.
    """
    scholarships = Scholarship.query.filter_by(is_active=True).all()
    results = []

    for s in scholarships:
        s_dict = s.to_dict()
        fit = calculate_fit_score(student_data, s_dict)

        if fit['score'] > 0:
            result = {
                **s_dict,
                'fit_score': fit['score'],
                'selection_probability': fit['probability'],
                'eligible': fit['eligible'],
                'eligibility_reasons': fit['reasons'],
                'disqualifiers': fit['disqualifiers'],
                'recommendation_rank': 0,
            }
            results.append(result)

    # Sort by fit score descending
    results.sort(key=lambda x: (-x['fit_score'], x.get('days_left', 999)))

    # Add rank
    for i, r in enumerate(results[:limit]):
        r['recommendation_rank'] = i + 1
        from datetime import date
        if r.get('deadline'):
            try:
                dl = date.fromisoformat(r['deadline'])
                r['days_left'] = (dl - date.today()).days
            except Exception:
                r['days_left'] = None

    return results[:limit]
