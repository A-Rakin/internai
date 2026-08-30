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


def generate_cover_letter(student_profile, internship):
    """
    Generate a tailored cover letter using AI based on student profile
    and internship requirements.
    """
    groq_api_key = getattr(settings, 'GROQ_API_KEY', '')

    student_info = (
        f"Name: {student_profile.user.get_full_name()}\n"
        f"University: {student_profile.university}\n"
        f"Department: {student_profile.department}\n"
        f"Education Level: {student_profile.get_education_level_display() if student_profile.education_level else 'N/A'}\n"
        f"Skills: {student_profile.skills}\n"
        f"Experience: {student_profile.experience}\n"
        f"GPA: {student_profile.gpa or 'N/A'}\n"
    )

    internship_info = (
        f"Title: {internship.title}\n"
        f"Company: {internship.company.company_name}\n"
        f"Industry: {internship.company.get_industry_display() if internship.company.industry else 'N/A'}\n"
        f"Required Skills: {internship.skills_required}\n"
        f"Requirements: {internship.requirements}\n"
        f"Description: {internship.description[:500]}\n"
    )

    if groq_api_key and not groq_api_key.startswith('gsk_your_groq'):
        try:
            from groq import Groq
            client = Groq(api_key=groq_api_key)

            prompt = f"""
Write a professional, compelling internship cover letter (200-300 words) based on:

STUDENT PROFILE:
{student_info}

INTERNSHIP POSITION:
{internship_info}

Guidelines:
- Address it to the hiring manager at {internship.company.company_name}
- Open with enthusiasm for the specific role
- Connect student's skills and experience to the job requirements
- Mention relevant coursework or projects
- Close with a call to action
- Professional but not overly formal tone
- Do NOT include placeholders like [Your Name] — use the student's actual name
"""
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert career counselor. Write polished, personalized cover letters."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )
            return response.choices[0].message.content

        except Exception as e:
            print(f"Groq Cover Letter Error: {e}")

    # Fallback template-based cover letter
    skills_list = student_profile.get_skills_list()
    matched = [s for s in skills_list if s.lower() in internship.skills_required.lower()]

    return (
        f"Dear Hiring Manager at {internship.company.company_name},\n\n"
        f"I am writing to express my enthusiastic interest in the {internship.title} internship position "
        f"at {internship.company.company_name}. As a {student_profile.get_education_level_display() if student_profile.education_level else ''} "
        f"student at {student_profile.university or 'my university'}, studying {student_profile.department or 'my field'}, "
        f"I am eager to apply my academic knowledge in a professional setting.\n\n"
        f"My technical skill set includes {', '.join(skills_list[:5]) if skills_list else 'various relevant technologies'}, "
        f"which align well with the requirements for this role. "
        f"{'I am particularly confident in ' + ', '.join(matched[:3]) + ' which are directly relevant to this position. ' if matched else ''}"
        f"{'My previous experience includes ' + student_profile.experience[:200] + '. ' if student_profile.experience else ''}\n\n"
        f"I am particularly drawn to {internship.company.company_name} because of the opportunity to work on "
        f"meaningful projects and grow professionally. I am confident that my passion for learning "
        f"and strong work ethic would make me a valuable addition to your team.\n\n"
        f"Thank you for considering my application. I look forward to discussing how I can contribute "
        f"to your team.\n\n"
        f"Sincerely,\n"
        f"{student_profile.user.get_full_name()}"
    )


def generate_interview_questions(internship):
    """
    Generate role-specific practice interview questions using AI.
    Returns a list of 5 questions.
    """
    groq_api_key = getattr(settings, 'GROQ_API_KEY', '')

    if groq_api_key and not groq_api_key.startswith('gsk_your_groq'):
        try:
            from groq import Groq
            client = Groq(api_key=groq_api_key)

            prompt = f"""
Generate exactly 5 interview questions for this internship position:

Title: {internship.title}
Required Skills: {internship.skills_required}
Requirements: {internship.requirements}
Description: {internship.description[:500]}

Mix of:
- 2 technical questions related to the required skills
- 1 behavioral/situational question
- 1 problem-solving question
- 1 motivation/fit question

Respond ONLY with a valid JSON array of 5 question strings. Example:
["Question 1?", "Question 2?", "Question 3?", "Question 4?", "Question 5?"]
"""
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert HR interviewer. Respond in valid JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)
            # Handle various response formats
            if isinstance(result, list):
                return result[:5]
            elif isinstance(result, dict):
                for key in ['questions', 'interview_questions', 'data']:
                    if key in result and isinstance(result[key], list):
                        return result[key][:5]
            return list(result.values())[:5] if isinstance(result, dict) else []

        except Exception as e:
            print(f"Groq Interview Questions Error: {e}")

    # Fallback questions
    title = internship.title.lower()
    skills = internship.skills_required or ''

    questions = [
        f"Tell me about yourself and why you're interested in the {internship.title} position.",
        f"What relevant skills or projects do you have that make you a good fit for this role?",
        "Describe a challenging project you've worked on. What was your role and what was the outcome?",
        "How do you handle tight deadlines and competing priorities?",
        f"Where do you see yourself in 5 years, and how does this internship at {internship.company.company_name} fit into your plans?",
    ]

    if 'python' in skills.lower() or 'django' in skills.lower():
        questions[1] = "Explain the difference between a list and a tuple in Python. When would you use each?"
    elif 'javascript' in skills.lower() or 'react' in skills.lower():
        questions[1] = "What is the Virtual DOM in React and why is it important for performance?"
    elif 'data' in title or 'machine learning' in title:
        questions[1] = "Explain the difference between supervised and unsupervised learning with examples."

    return questions


def grade_interview_answer(question, answer, internship):
    """
    Grade a practice interview answer using AI.
    Returns a dict with score (1-10) and feedback.
    """
    groq_api_key = getattr(settings, 'GROQ_API_KEY', '')

    if groq_api_key and not groq_api_key.startswith('gsk_your_groq'):
        try:
            from groq import Groq
            client = Groq(api_key=groq_api_key)

            prompt = f"""
Grade this interview answer for the {internship.title} position:

QUESTION: {question}
ANSWER: {answer}

Respond ONLY with a valid JSON object:
{{
    "score": <integer 1-10>,
    "feedback": "<2-3 sentences of constructive feedback>",
    "strengths": "<what the candidate did well>",
    "improvement": "<specific suggestion for improvement>"
}}
"""
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert HR interviewer. Grade answers honestly. Respond in valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.3,
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            print(f"Groq Grading Error: {e}")

    # Fallback grading
    word_count = len(answer.split())
    if word_count < 20:
        score = 3
        feedback = "Your answer is too brief. Try to provide more detail and examples."
    elif word_count < 50:
        score = 5
        feedback = "Your answer covers the basics but could benefit from more specific examples."
    elif word_count < 100:
        score = 7
        feedback = "Good answer with reasonable detail. Consider adding a concrete example from your experience."
    else:
        score = 8
        feedback = "Comprehensive answer with good detail. Focus on being more concise while maintaining key points."

    return {
        'score': score,
        'feedback': feedback,
        'strengths': 'Shows willingness to engage with the question.',
        'improvement': 'Add specific examples from projects or coursework to strengthen your response.',
    }

