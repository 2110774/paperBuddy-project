# Funding Planner AI
# Optimizes funding sources to cover total education fee


def generate_funding_plan(student_data: dict, total_fee: float) -> dict:
    """
    Generate an optimal funding plan for a student.
    Distributes total fee across scholarships, CSR, NGO, loans, and installments.
    """
    income = student_data.get('annual_income') or 0
    cgpa = student_data.get('cgpa') or 0
    category = (student_data.get('category') or '').upper()
    disability = student_data.get('disability_status') or False
    state = student_data.get('state') or ''
    degree = (student_data.get('degree') or '').lower()

    plan = {
        'total_fee': total_fee,
        'government_scholarship': 0,
        'csr_funding': 0,
        'ngo_funding': 0,
        'loan_amount': 0,
        'crowdfunding': 0,
        'installments': 0,
        'funding_gap': 0,
        'breakdown': [],
        'timeline': [],
        'tips': [],
    }

    remaining = total_fee

    # 1. Government Scholarship estimate
    if income <= 250000:
        if category in ['SC', 'ST']:
            govt_scholarship = min(remaining, total_fee * 0.70)
            plan['breakdown'].append({
                'source': 'Government Scholarship (SC/ST Post-Matric)',
                'amount': govt_scholarship,
                'probability': 0.85,
                'apply_link': 'https://scholarships.gov.in',
                'deadline': 'October 31',
                'action': 'Apply on NSP Portal with caste certificate',
            })
        elif category == 'OBC':
            govt_scholarship = min(remaining, total_fee * 0.50)
            plan['breakdown'].append({
                'source': 'Government Scholarship (OBC Post-Matric)',
                'amount': govt_scholarship,
                'probability': 0.75,
                'apply_link': 'https://scholarships.gov.in',
                'deadline': 'October 31',
                'action': 'Apply on NSP Portal with OBC certificate',
            })
        else:
            govt_scholarship = min(remaining, total_fee * 0.35)
            plan['breakdown'].append({
                'source': 'Central Sector Scholarship (General/EWS)',
                'amount': govt_scholarship,
                'probability': 0.60,
                'apply_link': 'https://scholarships.gov.in',
                'deadline': 'November 30',
                'action': 'Apply on NSP Portal — high income check',
            })
    elif income <= 600000:
        govt_scholarship = min(remaining, total_fee * 0.25)
        plan['breakdown'].append({
            'source': 'Merit-cum-Means Scholarship',
            'amount': govt_scholarship,
            'probability': 0.55,
            'apply_link': 'https://scholarships.gov.in',
            'deadline': 'November 30',
            'action': 'Apply with income certificate and merit proof',
        })
    else:
        govt_scholarship = min(remaining, total_fee * 0.10)

    plan['government_scholarship'] = round(govt_scholarship)
    remaining -= govt_scholarship

    if remaining <= 0:
        plan['funding_gap'] = 0
        return _finalize_plan(plan, total_fee)

    # 2. CSR Funding
    if cgpa >= 7.0 and income <= 600000:
        csr = min(remaining, total_fee * 0.20)
        plan['csr_funding'] = round(csr)
        plan['breakdown'].append({
            'source': 'CSR Scholarship (Corporate Social Responsibility)',
            'amount': csr,
            'probability': 0.65,
            'examples': ['Tata Scholarship', 'Infosys Catch Them Young', 'Mahindra Nanhi Kali'],
            'action': 'Apply directly on company websites or via Buddy4Study',
        })
        remaining -= csr

    # 3. NGO Funding
    if income <= 400000 and remaining > 0:
        ngo = min(remaining, total_fee * 0.15)
        plan['ngo_funding'] = round(ngo)
        plan['breakdown'].append({
            'source': 'NGO Support Funding',
            'amount': ngo,
            'probability': 0.50,
            'examples': ['CRY', 'Akanksha Foundation', 'Teach For India', 'Local NGOs'],
            'action': 'Contact NGOs in your city with financial need proof',
        })
        remaining -= ngo

    # 4. Education Loan
    if remaining > 0 and income > 0:
        loan_limit = min(remaining, 1000000)  # Max ₹10 lakh
        if loan_limit > 0:
            plan['loan_amount'] = round(loan_limit * 0.7)
            plan['breakdown'].append({
                'source': 'Education Loan (SBI/HDFC Credila)',
                'amount': plan['loan_amount'],
                'probability': 0.80,
                'interest_rate': '8.5–11% p.a.',
                'moratorium': 'Course duration + 1 year',
                'action': 'Apply at your nearest SBI branch or online at sbi.co.in',
            })
            remaining -= plan['loan_amount']

    # 5. Crowdfunding
    if remaining > 5000 and income <= 300000:
        crowd = min(remaining, 50000)
        plan['crowdfunding'] = round(crowd)
        plan['breakdown'].append({
            'source': 'Crowdfunding Campaign',
            'amount': crowd,
            'probability': 0.40,
            'platforms': ['Milaap.org', 'Ketto.org', 'ImpactGuru'],
            'action': 'Create a fundraiser with your story and share on social media',
        })
        remaining -= crowd

    # 6. Installment Plan
    if remaining > 0:
        plan['installments'] = round(remaining * 0.6)
        plan['breakdown'].append({
            'source': 'EMI / Installment Plan with Institution',
            'amount': plan['installments'],
            'probability': 0.90,
            'action': 'Request installment plan from your institution\'s finance office',
        })
        remaining -= plan['installments']

    plan['funding_gap'] = max(0, round(remaining))

    # Timeline
    plan['timeline'] = [
        {'month': 1, 'action': 'Apply for Government Scholarship on NSP', 'priority': 'high'},
        {'month': 1, 'action': 'Submit income and caste certificates', 'priority': 'high'},
        {'month': 2, 'action': 'Apply for CSR scholarships', 'priority': 'medium'},
        {'month': 2, 'action': 'Contact local NGOs for support', 'priority': 'medium'},
        {'month': 3, 'action': 'Apply for education loan at bank', 'priority': 'high'},
        {'month': 4, 'action': 'Start crowdfunding campaign if needed', 'priority': 'low'},
        {'month': 5, 'action': 'Negotiate installment plan with institution', 'priority': 'medium'},
    ]

    # Tips
    plan['tips'] = [
        'Apply for ALL scholarships you qualify for — don\'t rely on just one source.',
        'Keep all documents updated: income certificate validity is 6 months.',
        'Monitor NSP portal regularly for new scholarship notifications.',
        'Maintain above 75% attendance to stay eligible for most scholarships.',
    ]

    return _finalize_plan(plan, total_fee)


def _finalize_plan(plan: dict, total_fee: float) -> dict:
    funded = (plan['government_scholarship'] + plan['csr_funding'] +
              plan['ngo_funding'] + plan['loan_amount'] +
              plan['crowdfunding'] + plan['installments'])
    plan['total_funded'] = round(funded)
    plan['funding_coverage_pct'] = round((funded / total_fee * 100) if total_fee > 0 else 0, 1)
    return plan
