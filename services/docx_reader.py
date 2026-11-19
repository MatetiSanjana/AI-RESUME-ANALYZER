"""
docx_reader.py
--------------
Single responsibility: extract raw text from a DOCX resume file.
"""

from docx import Document


def extract_text_from_docx(file_path):
    """
    Read a DOCX file and return its full text content as a single string.
    Includes text from paragraphs and table cells.
    """
    text_parts = []
    try:
        document = Document(file_path)

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)

        for table in document.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        text_parts.append(cell.text)

    except Exception as e:
        raise ValueError(f"Could not read DOCX file: {e}")

    return "\n".join(text_parts).strip()
