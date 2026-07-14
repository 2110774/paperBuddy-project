# Essay Generator — Template-based scholarship essay generation
# No external API required

import random

ESSAY_TEMPLATES = {
    'scholarship_essay': [
        """My name is {name}, and I am a {year} year {degree} student specializing in {branch} at {institution}. Growing up in {state}, education was never taken for granted in our household. With a family income of approximately ₹{income} per year, every opportunity to learn has been a gift earned through sacrifice and perseverance.

Despite financial constraints, I have maintained a CGPA of {cgpa}, demonstrating my commitment to academic excellence. My achievements include {achievements}. I believe that education is the most powerful tool to break the cycle of poverty, and {scholarship_name} would be the key that unlocks my full potential.

The scholarship amount will help me {purpose}. I am committed to using this opportunity not just for personal growth, but to give back to my community by mentoring students like me in the future.

I humbly request your committee to consider my application and invest in my journey towards a brighter future.""",

        """Education is the foundation upon which dreams are built. As a first-generation college student from {state}, I have witnessed firsthand how access to quality education can transform lives.

I am {name}, pursuing {degree} in {branch} from {institution}. Maintaining a CGPA of {cgpa} while managing financial pressures has taught me resilience and determination. {achievements}

{scholarship_name} would be more than financial support — it would be a vote of confidence in my potential. With this scholarship, I plan to {purpose}, and ultimately contribute back to society through my work.

I am not asking for charity — I am asking for the opportunity to prove that with the right support, students from every background can achieve excellence."""
    ],
    'sop': [
        """Statement of Purpose

I am applying for {scholarship_name} to support my {degree} program in {branch}. My academic journey has been driven by curiosity and a desire to create impact in {branch}.

Academic Background: With a CGPA of {cgpa} from {institution}, I have demonstrated consistent academic performance. {achievements}

Financial Need: My family's annual income of ₹{income} makes it challenging to meet educational expenses. This scholarship would directly cover {purpose}.

Future Goals: Upon completion of my degree, I plan to pursue a career in {career_goal}, contributing to India's growth in {branch}.

I am confident that with {scholarship_name}'s support, I will not only excel academically but also become a role model for students from similar backgrounds."""
    ],
    'motivation_letter': [
        """To the Scholarship Committee,

I write to you with great enthusiasm about {scholarship_name}. As a {year} year student at {institution}, this opportunity aligns perfectly with both my academic journey and personal circumstances.

What drives me: {branch} is not just my field of study — it is my passion. I have dedicated myself to understanding its nuances, as evidenced by my CGPA of {cgpa}. {achievements}

What holds me back: Financial constraints have often tested my resolve. Our family's income of ₹{income} per year leaves little room for educational expenses.

What this scholarship means: {scholarship_name} would allow me to {purpose}, freeing me to focus entirely on my academic goals.

I am committed to making the most of this opportunity and representing the values of your organization through excellence in my work.

Respectfully,
{name}"""
    ]
}


def generate_essay(essay_type: str, context: dict) -> dict:
    """
    Generate a scholarship essay using templates.
    """
    valid_types = ['scholarship_essay', 'sop', 'motivation_letter', 'personal_statement']
    if essay_type not in valid_types:
        essay_type = 'scholarship_essay'

    if essay_type == 'personal_statement':
        essay_type = 'scholarship_essay'

    templates = ESSAY_TEMPLATES.get(essay_type, ESSAY_TEMPLATES['scholarship_essay'])
    template = random.choice(templates)

    # Fill in template variables
    filled = template.format(
        name=context.get('name', 'the applicant'),
        year=_ordinal(context.get('year_of_study', 1)),
        degree=context.get('degree', 'undergraduate'),
        branch=context.get('branch', 'Engineering'),
        institution=context.get('institution', 'my institution'),
        state=context.get('state', 'my home state'),
        income=f"{int(context.get('annual_income', 0) or 0):,}",
        cgpa=context.get('cgpa', '7.5'),
        achievements=context.get('achievements', 'I have been actively involved in academic and extracurricular activities'),
        scholarship_name=context.get('scholarship_name', 'this scholarship'),
        purpose=context.get('purpose', 'cover my tuition fees and focus on my studies without financial stress'),
        career_goal=context.get('career_goal', 'my chosen field'),
    )

    word_count = len(filled.split())

    return {
        'essay': filled,
        'essay_type': essay_type,
        'word_count': word_count,
        'tips': [
            'Personalize this essay with specific examples from your life.',
            'Add concrete numbers and achievements where possible.',
            'Proofread for grammar and spelling before submitting.',
            'Ask a teacher or mentor to review the essay.',
            'Adjust the purpose section to match the specific scholarship criteria.',
        ]
    }


def _ordinal(n: int) -> str:
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    return f"{n}{suffixes.get(n % 10, 'th') if n % 100 not in range(11, 14) else 'th'}"
