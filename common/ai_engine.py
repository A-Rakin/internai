"""
============================================================
InternAI - AI Resume Parsing & Match Scoring Engine
============================================================
Extracts text from uploaded PDF resumes and calculates a
skills-compatibility match score (0-100%) against internship role criteria.
Supports Groq Cloud API (llama-3.3-70b-versatile) with automatic local fallback.
============================================================
"""

import re
import json
from pypdf import PdfReader
from django.conf import settings


def extract_text_from_pdf(pdf_file):
    """
    Extract text content from an uploaded PDF file stream or file path.
    Returns plain text as a string.
    """
    text = ""
    try:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
    return text


def calculate_skill_match(resume_text, internship):
    """
    Calculate an AI Match Score (0-100%) comparing the candidate's resume text
    against the internship's required skills, title, and requirements.

    Attempts Groq Cloud API first if GROQ_API_KEY is present in settings,
    otherwise falls back to high-performance local NLP keyword matching.
    """
    if not resume_text:
        return {
            'score': 70,
            'matched_skills': [],
            'missing_skills': [],
            'recommendation': 'Standard applicant evaluation.',
        }

    groq_api_key = getattr(settings, 'GROQ_API_KEY', '')

    # Try Groq Cloud API if key is available
    if groq_api_key and not groq_api_key.startswith('gsk_your_groq'):
        try:
            from groq import Groq
            client = Groq(api_key=groq_api_key)

            prompt = f"""
You are an expert HR AI Recruiter. Analyze this candidate's resume text against the following internship position:

INTERNSHIP POSITION:
Title: {internship.title}
Required Skills: {internship.skills_required}
Role Requirements: {internship.requirements}

RESUME TEXT:
{resume_text[:3000]}

Respond ONLY with a valid JSON object matching this exact schema:
{{
    "score": <integer score from 50 to 98 based on match fit>,
    "matched_skills": [<list of matching skill strings found in resume>],
    "missing_skills": [<list of missing required skills>],
    "recommendation": "<1-2 sentence professional recruiter summary of fit>"
}}
"""

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a professional AI recruiter. Respond in valid JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            response_content = response.choices[0].message.content
            ai_data = json.loads(response_content)

            return {
                'score': int(ai_data.get('score', 75)),
                'matched_skills': ai_data.get('matched_skills', []),
                'missing_skills': ai_data.get('missing_skills', []),
                'recommendation': ai_data.get('recommendation', 'Evaluated by Groq Cloud AI LLM.'),
            }

        except Exception as e:
            print(f"Groq API Call Error (falling back to local matcher): {e}")

    # Fallback to local NLP matcher
    return _local_skill_match(resume_text, internship)


def _local_skill_match(resume_text, internship):
    """Local fallback keyword & NLP matching engine."""
    resume_text_lower = resume_text.lower()

    required_skills = internship.get_skills_list()
    if not required_skills:
        req_words = [w.strip() for w in re.split(r'[,;\n.]', internship.requirements) if len(w.strip()) > 2]
        required_skills = req_words[:8]

    matched_skills = []
    missing_skills = []

    for skill in required_skills:
        skill_clean = skill.strip()
        if not skill_clean:
            continue
        pattern = r'\b' + re.escape(skill_clean.lower()) + r'\b'
        if re.search(pattern, resume_text_lower):
            matched_skills.append(skill_clean)
        else:
            missing_skills.append(skill_clean)

    if required_skills:
        skills_ratio = len(matched_skills) / len(required_skills)
    else:
        skills_ratio = 0.8

    title_words = [w.lower() for w in internship.title.split() if len(w) > 3]
    title_matches = sum(1 for w in title_words if w in resume_text_lower)
    title_bonus = (title_matches / max(len(title_words), 1)) * 15

    raw_score = (skills_ratio * 75) + title_bonus + 10
    final_score = int(min(max(raw_score, 50), 98))

    if final_score >= 85:
        recommendation = "Strong Match: Candidate possesses the core technical skills and background required for this position."
    elif final_score >= 70:
        recommendation = "Good Match: Candidate fulfills key requirements with potential for fast onboarding."
    else:
        recommendation = "Moderate Match: Candidate matches partial criteria; review cover letter and experience details."

    return {
        'score': final_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'recommendation': recommendation,
    }
