"""
report_service.py
------------------
Single responsibility: generate a downloadable PDF report
summarizing the resume analysis results.
"""

import os
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from config import Config


class ReportPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "AI Resume Analyzer - Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(4)


def _write_section(pdf, title, items):
    """Helper to write a titled bullet-list section into the PDF."""
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)

    if not items:
        pdf.cell(0, 6, "  - None", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    else:
        for item in items:
            # encode/decode to avoid unicode issues with core PDF fonts
            safe_item = str(item).encode("latin-1", "replace").decode("latin-1")
            pdf.multi_cell(0, 6, f"  - {safe_item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)


def generate_pdf_report(candidate_name, resume_score, ats_score,
                         matched_skills, missing_skills, feedback, filename):
    """
    Build a PDF report and save it to the reports/ folder.
    Returns the full path of the generated file.
    """
    pdf = ReportPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Candidate Name: {candidate_name or 'N/A'}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 8, f"Resume Score: {resume_score}/100", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if ats_score is not None:
        pdf.cell(0, 8, f"ATS Score: {ats_score}/100", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    _write_section(pdf, "Matched Skills", matched_skills)
    _write_section(pdf, "Missing Skills", missing_skills)
    _write_section(pdf, "Strengths", feedback.get("strengths", []))
    _write_section(pdf, "Weaknesses", feedback.get("weaknesses", []))
    _write_section(pdf, "Resume Improvement Suggestions", feedback.get("resume_suggestions", []))
    _write_section(pdf, "Skills to Learn", feedback.get("skills_to_learn", []))
    _write_section(pdf, "ATS Improvement Tips", feedback.get("ats_tips", []))

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Overall Feedback", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 11)
    overall = str(feedback.get("overall_feedback", "")).encode("latin-1", "replace").decode("latin-1")
    pdf.multi_cell(0, 6, overall, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    os.makedirs(Config.REPORT_FOLDER, exist_ok=True)
    output_path = os.path.join(Config.REPORT_FOLDER, filename)
    pdf.output(output_path)

    return output_path
