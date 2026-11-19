"""
analyze_routes.py
------------------
Blueprint that handles the core analysis pipeline:
1. Validate + save uploaded resume
2. Parse resume (services/resume_parser.py)
3. If JD provided, extract JD skills + calculate ATS score
4. Generate Gemini feedback
5. Save summary to database
6. Store full results in session and redirect to /result
"""

import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from config import Config
from utils.file_validator import allowed_file, is_valid_size
from utils.helpers import current_timestamp
from utils.db_helper import insert_resume, insert_analysis
from services.resume_parser import parse_resume
from services.gemini_service import extract_jd_skills, generate_feedback
from services.ats_service import calculate_ats_score, calculate_resume_score

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files.get("resume")
    jd_text = request.form.get("jd_text", "").strip()
    company_name = request.form.get("company_name", "").strip()

    # --- Validate uploaded file ---
    if not resume_file or resume_file.filename == "":
        flash("Please upload a resume file.")
        return redirect(url_for("main.upload_page"))

    if not allowed_file(resume_file.filename):
        flash("Only PDF and DOCX files are allowed.")
        return redirect(url_for("main.upload_page"))

    if not is_valid_size(resume_file.stream):
        flash("File is too large. Max size is 5MB.")
        return redirect(url_for("main.upload_page"))

    # --- Save file to uploads/ ---
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    save_path = os.path.join(Config.UPLOAD_FOLDER, resume_file.filename)
    resume_file.save(save_path)

    try:
        # --- Step 1: Parse resume into structured data ---
        raw_text, resume_data = parse_resume(save_path, resume_file.filename)

        # --- Step 2: Resume score (always calculated) ---
        resume_score = calculate_resume_score(resume_data)

        ats_result = None
        jd_skills = []

        # --- Step 3: If JD provided, calculate ATS score ---
        if jd_text:
            jd_skills_data = extract_jd_skills(jd_text)
            jd_skills = jd_skills_data.get("skills", [])
            ats_result = calculate_ats_score(resume_data, jd_skills)

        # --- Step 4: Gemini feedback (uses ATS results if available) ---
        feedback = generate_feedback(
            resume_data=resume_data,
            jd_text=jd_text,
            ats_score=ats_result["ats_score"] if ats_result else None,
            matched_skills=ats_result["matched_skills"] if ats_result else [],
            missing_skills=ats_result["missing_skills"] if ats_result else [],
        )

        # --- Step 5: Save to database ---
        resume_id = insert_resume(
            candidate_name=resume_data.get("name", ""),
            email=resume_data.get("email", ""),
            phone=resume_data.get("phone", ""),
            resume_score=resume_score,
            upload_date=current_timestamp(),
        )

        if ats_result:
            insert_analysis(
                resume_id=resume_id,
                company_name=company_name,
                ats_score=ats_result["ats_score"],
                can_apply=ats_result["can_apply"],
                analysis_date=current_timestamp(),
            )

        # --- Step 6: Store results in session for /result and /download-report ---
        session["result"] = {
            "resume_id": resume_id,
            "candidate_name": resume_data.get("name", ""),
            "resume_score": resume_score,
            "extracted_skills": resume_data.get("skills", []),
            "has_jd": bool(jd_text),
            "ats_score": ats_result["ats_score"] if ats_result else None,
            "matched_skills": ats_result["matched_skills"] if ats_result else [],
            "missing_skills": ats_result["missing_skills"] if ats_result else [],
            "match_percentage": ats_result["match_percentage"] if ats_result else None,
            "can_apply": ats_result["can_apply"] if ats_result else None,
            "feedback": feedback,
        }

        return redirect(url_for("result.result_page"))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for("main.upload_page"))
    except Exception:
        flash("Something went wrong while analyzing the resume. Please try again.")
        return redirect(url_for("main.upload_page"))
