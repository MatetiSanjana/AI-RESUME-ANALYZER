"""
result_routes.py
-----------------
Blueprint for showing the analysis result page and
generating/downloading the PDF report from that result.
"""

from flask import Blueprint, render_template, session, redirect, url_for, flash, send_file

from services.report_service import generate_pdf_report

result_bp = Blueprint("result", __name__)


@result_bp.route("/result")
def result_page():
    """Display the stored analysis result (set by /analyze)."""
    result = session.get("result")
    if not result:
        flash("No analysis found. Please upload a resume first.")
        return redirect(url_for("main.upload_page"))

    return render_template("result.html", result=result)


@result_bp.route("/download-report")
def download_report():
    """Generate a PDF from the session result and send it to the user."""
    result = session.get("result")
    if not result:
        flash("No analysis found. Please upload a resume first.")
        return redirect(url_for("main.upload_page"))

    filename = f"resume_report_{result['resume_id']}.pdf"

    output_path = generate_pdf_report(
        candidate_name=result.get("candidate_name"),
        resume_score=result.get("resume_score"),
        ats_score=result.get("ats_score"),
        matched_skills=result.get("matched_skills", []),
        missing_skills=result.get("missing_skills", []),
        feedback=result.get("feedback", {}),
        filename=filename,
    )

    return send_file(output_path, as_attachment=True, download_name=filename)
