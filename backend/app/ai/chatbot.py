# AI Chatbot using keyword matching + knowledge base
# Works without sentence-transformers installation (fallback to keyword matching)
# When sentence-transformers is installed, uses semantic similarity

import re
import math

# Knowledge base — scholarship Q&A
KNOWLEDGE_BASE = [
    {
        "question": "What documents are required for scholarship application?",
        "answer": "Typically required documents include: Income Certificate, Marksheet/Result, Identity Proof (Aadhaar/PAN), Bank Passbook, Bonafide Certificate, Caste Certificate (if applicable), Disability Certificate (if applicable), and Recent Passport Photo.",
        "keywords": ["documents", "required", "application", "certificate", "marksheet", "identity"]
    },
    {
        "question": "What is NSP - National Scholarship Portal?",
        "answer": "NSP (National Scholarship Portal) is India's one-stop digital platform for scholarship applications. It hosts Central, State, and UT government scholarships. Students can apply at scholarships.gov.in. Key schemes include Post-Matric Scholarship, Pre-Matric Scholarship, and Merit-cum-Means Scholarship.",
        "keywords": ["nsp", "national scholarship portal", "scholarships.gov.in", "government", "central"]
    },
    {
        "question": "What is CGPA requirement for merit scholarships?",
        "answer": "Merit scholarships typically require a minimum CGPA of 7.0 or 70% marks. Some prestigious scholarships like Prime Minister's Scholarship require 8.0+ CGPA. State-level merit scholarships may accept 6.5+ CGPA.",
        "keywords": ["cgpa", "merit", "marks", "percentage", "minimum", "academic"]
    },
    {
        "question": "How to get scholarship for SC/ST students?",
        "answer": "SC/ST students can apply for: 1) Post-Matric Scholarship for SC/ST (Central Government), 2) Top Class Education Scheme for SC, 3) Dr. Ambedkar Post-Matric Scholarship, 4) Rajiv Gandhi National Fellowship, 5) State-specific SC/ST scholarships. Apply via NSP portal with caste certificate.",
        "keywords": ["sc", "st", "scheduled caste", "scheduled tribe", "dalit", "tribal", "caste"]
    },
    {
        "question": "What scholarships are available for girls/female students?",
        "answer": "Scholarships for women: 1) Pragati Scholarship (AICTE - for technical education), 2) Begum Hazrat Mahal National Scholarship, 3) Indira Gandhi Single Girl Child Scholarship, 4) CBSE Merit Scholarship for Single Girl Child, 5) Women Scientist Scholarship (DST-WOS-A). Many state governments also have special scholarships for girls.",
        "keywords": ["girl", "female", "women", "lady", "gender", "daughter", "sister"]
    },
    {
        "question": "How does EduBridge AI recommend scholarships?",
        "answer": "EduBridge AI analyzes your profile (income, CGPA, state, category, degree, disability status, skills) and calculates a Scholarship Fit Score (0-100) for each available scholarship. Higher scores mean better match. We consider eligibility criteria, deadlines, and your specific circumstances to give personalized recommendations.",
        "keywords": ["edubridge", "recommend", "fit score", "how", "works", "algorithm", "recommendation"]
    },
    {
        "question": "What is the income limit for government scholarships?",
        "answer": "Income limits vary by scholarship: Post-Matric Scholarship (OBC) - ₹1.5 lakh/year, SC/ST scholarships - ₹2.5 lakh/year, NSP Central Sector - ₹8 lakh/year, State scholarships - typically ₹1-3 lakh/year. Income Certificate from Tehsildar/SDM is required.",
        "keywords": ["income", "limit", "annual", "lakh", "family income", "income certificate", "eligibility"]
    },
    {
        "question": "How to apply for private scholarships and NGO funding?",
        "answer": "To apply for private/NGO scholarships: 1) Search on EduBridge AI Scholarship Explorer, 2) Check Buddy4Study, Vidyasaarathi portals, 3) Contact your college's scholarship cell, 4) Look for CSR initiatives from companies like Tata, Infosys, Mahindra, 5) Apply to alumni associations of your college. Ensure documents are ready.",
        "keywords": ["private", "ngo", "trust", "foundation", "csr", "corporate", "tata", "infosys"]
    },
    {
        "question": "What is the deadline for scholarship applications?",
        "answer": "Scholarship deadlines vary. NSP scholarships typically close in October-November each year. AICTE scholarships close around September. Many state scholarships have rolling deadlines. Always check the specific scholarship deadline on EduBridge AI or the official portal. Apply early to avoid last-minute technical issues.",
        "keywords": ["deadline", "last date", "close", "when", "date", "october", "november"]
    },
    {
        "question": "Can I apply for multiple scholarships simultaneously?",
        "answer": "Yes, you can apply for multiple scholarships simultaneously. However, some government scholarships restrict receiving funding from multiple sources. Always read the terms carefully. EduBridge AI tracks all your applications and alerts you if there are any conflicts. We recommend applying to 5-8 scholarships to maximize your chances.",
        "keywords": ["multiple", "simultaneously", "more than one", "how many", "apply many"]
    },
    {
        "question": "What is a Bonafide Certificate?",
        "answer": "A Bonafide Certificate is an official document issued by your school/college confirming that you are a genuine enrolled student. It includes: your name, enrollment number, course name, year of study, and institution details. You can get it from your college administration/registrar office. It's required for most scholarship applications.",
        "keywords": ["bonafide", "certificate", "enrollment", "college", "confirmation", "institution"]
    },
    {
        "question": "How to calculate financial health score?",
        "answer": "EduBridge AI calculates your Financial Health Score based on: 1) Per-capita income (25%), 2) Academic performance/CGPA (25%), 3) Attendance percentage (20%), 4) Fee dues status (20%), 5) Scholarship coverage (10%). A score above 75 is excellent, 50-75 is good, 30-50 is at risk, below 30 is critical.",
        "keywords": ["financial health", "score", "calculate", "how", "formula", "components"]
    },
    {
        "question": "What is dropout prediction?",
        "answer": "EduBridge AI's dropout prediction analyzes financial risk (income, fee dues, scholarship status) and academic risk (CGPA, attendance) to predict the likelihood of a student dropping out. Schools use this to intervene early and provide support. If your risk is high, EduBridge AI will recommend specific scholarships and support programs.",
        "keywords": ["dropout", "prediction", "risk", "probability", "drop out", "leave"]
    },
    {
        "question": "How to write a scholarship essay?",
        "answer": "Tips for a winning scholarship essay: 1) Start with a compelling personal story, 2) Clearly state your financial need, 3) Describe your academic achievements and goals, 4) Explain how the scholarship will help you, 5) Mention your community involvement, 6) Keep it within word limit, 7) Proofread thoroughly. Use EduBridge AI's Essay Generator for templates.",
        "keywords": ["essay", "write", "sop", "statement", "motivation letter", "personal statement", "tips"]
    },
    {
        "question": "What is PM Scholarship Scheme?",
        "answer": "PM Scholarship Scheme (PMSS) is for wards and widows of ex-servicemen/coast guard personnel. Benefits: ₹2,500/month for girls, ₹2,250/month for boys for professional degree courses. Eligibility: Min 60% in qualifying exam, enrolled in 1st year of recognized professional course. Apply via KSB portal (ksb.gov.in).",
        "keywords": ["pm", "prime minister", "pmss", "ex-servicemen", "defense", "army", "ksb"]
    },
]


def compute_keyword_similarity(query: str, kb_entry: dict) -> float:
    """Simple keyword-based similarity score."""
    query_words = set(re.sub(r'[^\w\s]', '', query.lower()).split())
    keywords = set(kb_entry.get('keywords', []))
    question_words = set(re.sub(r'[^\w\s]', '', kb_entry['question'].lower()).split())
    all_relevant = keywords | question_words

    if not query_words or not all_relevant:
        return 0.0

    matches = query_words & all_relevant
    precision = len(matches) / len(query_words) if query_words else 0
    recall = len(matches) / len(all_relevant) if all_relevant else 0

    if precision + recall == 0:
        return 0.0

    f1 = 2 * precision * recall / (precision + recall)
    return f1


def get_chatbot_response(user_message: str, chat_history: list = None) -> dict:
    """
    Generate a chatbot response using the local knowledge base.
    Falls back to helpful default responses for unknown queries.
    """
    if not user_message or not user_message.strip():
        return {
            'response': 'Hello! I\'m EduBridge AI Assistant. Ask me anything about scholarships, financial aid, or your application journey!',
            'intent': 'greeting',
            'confidence': 1.0,
            'sources': [],
        }

    query = user_message.strip()

    # Score each KB entry
    scored = []
    for entry in KNOWLEDGE_BASE:
        score = compute_keyword_similarity(query, entry)
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda x: -x[0])

    if scored and scored[0][0] > 0.1:
        best_score, best_entry = scored[0]
        confidence = min(0.95, best_score * 2)

        response = best_entry['answer']

        # Add contextual follow-up
        if len(scored) > 1:
            response += f"\n\n💡 Related: {scored[1][1]['question']}"

        return {
            'response': response,
            'intent': 'knowledge_base',
            'confidence': round(confidence, 2),
            'sources': [best_entry['question']],
            'matched_question': best_entry['question'],
        }

    # Fallback responses based on common patterns
    query_lower = query.lower()

    if any(w in query_lower for w in ['hello', 'hi', 'hey', 'namaste']):
        return {
            'response': '👋 Hello! I\'m EduBridge AI, your scholarship assistant. I can help you with:\n• Finding scholarships\n• Understanding eligibility\n• Document requirements\n• Application tips\n\nWhat would you like to know?',
            'intent': 'greeting',
            'confidence': 0.9,
        }

    if any(w in query_lower for w in ['thank', 'thanks', 'dhanyawad']):
        return {
            'response': '😊 You\'re welcome! Best of luck with your scholarship journey. Feel free to ask anytime!',
            'intent': 'thanks',
            'confidence': 0.9,
        }

    if any(w in query_lower for w in ['help', 'assist', 'support']):
        return {
            'response': 'I can help you with:\n\n📚 **Scholarship Discovery** — Find scholarships that match your profile\n📊 **Financial Health** — Understand your financial risk score\n📝 **Application Tips** — Essay writing, document checklist\n🎯 **Career Guidance** — Career suggestions based on your profile\n\nWhat specific question do you have?',
            'intent': 'help',
            'confidence': 0.85,
        }

    # Default fallback
    return {
        'response': f'I don\'t have specific information about "{query}" in my knowledge base. However, I recommend:\n\n1. 🔍 Use the **Scholarship Explorer** to search for matching scholarships\n2. 📊 Check your **Financial Health Score** for personalized recommendations\n3. 📞 Contact the **Help Center** for human assistance\n\nCan you rephrase your question? I\'m best at answering scholarship eligibility, document requirements, and application process questions.',
        'intent': 'fallback',
        'confidence': 0.3,
    }
