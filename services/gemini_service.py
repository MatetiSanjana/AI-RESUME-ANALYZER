"""
gemini_service.py
------------------
Single responsibility: all communication with the Google Gemini API.

Gemini is used ONLY for intelligent/language tasks:
1. Extracting structured info from resume text
2. Extracting skills from a job description
3. Generating human-readable feedback

Gemini NEVER calculates the ATS score - that stays in ats_service.py (pure Python).
"""

import json
import re
import google.generativeai as genai
from config import Config

# Configure the Gemini client once using the API key from config
genai.configure(api_key=Config.GEMINI_API_KEY)

MODEL_NAME = "gemini-3.6-flash"


def _call_gemini(prompt):
    """
    Internal helper: sends a prompt to Gemini and returns the raw text response.
    Kept private (prefixed with _) since only this file should call the API directly.
    """
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()


def _extract_json(raw_text):
    """
    Gemini sometimes wraps JSON in ```json ``` code fences.
    This strips those and safely parses the JSON.
    """
    cleaned = re.sub(r"^```json|^```|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: try to find the first {...} block in the text
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError("Gemini did not return valid JSON")


def extract_resume_info(resume_text):
    """
    Ask Gemini to extract structured candidate info from resume text.
    Returns a dict: name, email, phone, skills, education, experience, projects
    """
    prompt = f"""
You are a resume parsing assistant. Extract structured information from the
resume text below and return ONLY valid JSON, no extra commentary, no markdown.

Return exactly this JSON structure:
{{
  "name": "",
  "email": "",
  "phone": "",
  "skills": [],
  "education": [],
  "experience": [],
  "projects": []
}}

Resume Text:
\"\"\"{resume_text}\"\"\"
"""
    raw = _call_gemini(prompt)
    data = _extract_json(raw)

    # Ensure all expected keys always exist, even if Gemini omits one
    defaults = {"name": "", "email": "", "phone": "", "skills": [],
                "education": [], "experience": [], "projects": []}
    defaults.update(data)
    return defaults


def extract_jd_skills(jd_text):
    """
    Ask Gemini to extract the important skills mentioned in a job description.
    Returns a dict: {"skills": [...]}
    """
    prompt = f"""
You are a job description analyzer. Read the job description below and
extract the important technical and soft skills required for the role.
Return ONLY valid JSON, no extra commentary, no markdown.

Return exactly this JSON structure:
{{
  "skills": []
}}

Job Description:
\"\"\"{jd_text}\"\"\"
"""
    raw = _call_gemini(prompt)
    data = _extract_json(raw)
    return {"skills": data.get("skills", [])}


def generate_feedback(resume_data, jd_text, ats_score, matched_skills, missing_skills):
    """
    Ask Gemini to generate human-readable feedback based on the resume,
    the (optional) job description, and the ATS results computed in Python.

    Returns a dict with: strengths, weaknesses, resume_suggestions,
    skills_to_learn, ats_tips, overall_feedback
    """
    jd_section = jd_text if jd_text else "No job description provided."

    prompt = f"""
You are a career coach AI. Based on the candidate data below, provide
constructive feedback. Return ONLY valid JSON, no extra commentary, no markdown.

Candidate Resume Data (JSON): {json.dumps(resume_data)}
Job Description: \"\"\"{jd_section}\"\"\"
ATS Score: {ats_score}
Matched Skills: {matched_skills}
Missing Skills: {missing_skills}

Return exactly this JSON structure:
{{
  "strengths": [],
  "weaknesses": [],
  "resume_suggestions": [],
  "skills_to_learn": [],
  "ats_tips": [],
  "overall_feedback": ""
}}
"""
    raw = _call_gemini(prompt)
    data = _extract_json(raw)

    defaults = {"strengths": [], "weaknesses": [], "resume_suggestions": [],
                "skills_to_learn": [], "ats_tips": [], "overall_feedback": ""}
    defaults.update(data)
    return defaults
