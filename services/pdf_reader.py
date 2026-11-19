"""
pdf_reader.py
-------------
Single responsibility: extract raw text from a PDF resume file.
"""

from PyPDF2 import PdfReader


def extract_text_from_pdf(file_path):
    """
    Read a PDF file and return its full text content as a single string.
    Pages are joined with newlines to preserve some structure.
    """
    text_parts = []
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
    except Exception as e:
        raise ValueError(f"Could not read PDF file: {e}")

    return "\n".join(text_parts).strip()
