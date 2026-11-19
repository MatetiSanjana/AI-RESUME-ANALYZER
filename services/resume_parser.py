"""
resume_parser.py
-----------------
Single responsibility: turn an uploaded resume file into structured data.

Flow:
1. Pick the correct reader (PDF or DOCX) based on file extension.
2. Get raw text from the file.
3. Send raw text to gemini_service for structured extraction.
"""

from services.pdf_reader import extract_text_from_pdf
from services.docx_reader import extract_text_from_docx
from services.gemini_service import extract_resume_info
from utils.file_validator import get_file_extension


def parse_resume(file_path, filename):
    """
    Given a saved resume file path, return:
    - raw_text: the plain extracted text (used later for ATS keyword search)
    - structured_data: dict from Gemini (name, email, phone, skills, etc.)
    """
    extension = get_file_extension(filename)

    if extension == "pdf":
        raw_text = extract_text_from_pdf(file_path)
    elif extension == "docx":
        raw_text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are allowed.")

    if not raw_text:
        raise ValueError("No readable text found in the uploaded resume.")

    structured_data = extract_resume_info(raw_text)

    return raw_text, structured_data
