"""
ats_service.py
---------------
Single responsibility: calculate ATS score and resume score using
plain Python logic only. Gemini is NEVER used for scoring - this
keeps the scoring transparent, deterministic, and easy to explain.
"""

from config import Config


def _normalize(skill):
    """Lowercase and strip a skill string for fair comparison."""
    return skill.strip().lower()


def compare_skills(resume_skills, jd_skills):
    """
    Compare resume skills against job description skills.
    Returns matched_skills, missing_skills, and match_percentage.
    """
    # Map normalized -> original casing (e.g. "sql" -> "SQL") so display
    # text keeps acronyms like "SQL"/"AWS" instead of becoming "Sql"/"Aws".
    resume_display = {_normalize(s): s.strip() for s in resume_skills if s}
    jd_display = {_normalize(s): s.strip() for s in jd_skills if s}

    resume_set = set(resume_display.keys())
    jd_set = set(jd_display.keys())

    if not jd_set:
        return [], [], 0.0

    matched = jd_set & resume_set
    missing = jd_set - resume_set

    match_percentage = round((len(matched) / len(jd_set)) * 100, 2)

    # Prefer the JD's original casing for display; fall back to resume's.
    matched_skills = sorted(jd_display.get(s, resume_display.get(s, s)) for s in matched)
    missing_skills = sorted(jd_display.get(s, s) for s in missing)

    return matched_skills, missing_skills, match_percentage


def calculate_ats_score(resume_data, jd_skills):
    """
    ATS Score = (Matched Skills / Total JD Skills) * 100
    Plus small bonus points for having Contact Info, Education,
    Experience, and Projects sections filled in.

    Returns: ats_score (int, capped at 100), matched_skills, missing_skills,
             match_percentage, can_apply ("YES"/"MAYBE"/"NO")
    """
    resume_skills = resume_data.get("skills", [])
    matched_skills, missing_skills, match_percentage = compare_skills(resume_skills, jd_skills)

    base_score = match_percentage

    # Bonus points (small, simple, explainable in an interview)
    bonus = 0
    if resume_data.get("email") or resume_data.get("phone"):
        bonus += 3
    if resume_data.get("education"):
        bonus += 3
    if resume_data.get("experience"):
        bonus += 2
    if resume_data.get("projects"):
        bonus += 2

    ats_score = min(round(base_score + bonus), 100)

    can_apply = determine_can_apply(ats_score)

    return {
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
        "can_apply": can_apply,
    }


def determine_can_apply(ats_score):
    """Map ATS score to a YES / MAYBE / NO recommendation."""
    if ats_score >= Config.ATS_YES_THRESHOLD:
        return "YES"
    elif ats_score >= Config.ATS_MAYBE_THRESHOLD:
        return "MAYBE"
    else:
        return "NO"


def calculate_resume_score(resume_data):
    """
    Calculate a general Resume Score (used when no JD is provided).
    Simple weighted scoring based on completeness of resume sections.
    Max score = 100.
    """
    score = 0

    if resume_data.get("name"):
        score += 10
    if resume_data.get("email"):
        score += 10
    if resume_data.get("phone"):
        score += 5
    if resume_data.get("skills"):
        score += min(len(resume_data["skills"]) * 3, 25)
    if resume_data.get("education"):
        score += 15
    if resume_data.get("experience"):
        score += 20
    if resume_data.get("projects"):
        score += 15

    return min(score, 100)
