"""
file_validator.py
------------------
Validates uploaded resume files before they are processed.
Keeps validation logic separate from route handlers.
"""

import os
from config import Config


def allowed_file(filename):
    """Check file extension is .pdf or .docx"""
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS


def get_file_extension(filename):
    """Return the lowercase extension of a filename without the dot."""
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


def is_valid_size(file_stream):
    """Ensure the uploaded file does not exceed the max allowed size."""
    file_stream.seek(0, os.SEEK_END)
    size = file_stream.tell()
    file_stream.seek(0)  # reset pointer for later reading
    return size <= Config.MAX_CONTENT_LENGTH
