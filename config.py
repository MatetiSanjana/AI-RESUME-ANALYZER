"""
config.py
----------
Central configuration file for the AI Resume Analyzer.
All paths, keys, and constants are defined here so that
no other file needs to hardcode values.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file (GEMINI_API_KEY etc.)
load_dotenv()

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Flask secret key (used for session/flash messages)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    # Gemini API key (loaded from .env, never hardcoded)
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

    # SQLite database file path
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "resume_analyzer.db")

    # Folder where uploaded resumes are stored
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # Folder where generated PDF reports are stored
    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

    # Allowed resume file types
    ALLOWED_EXTENSIONS = {"pdf", "docx"}

    # Max upload size: 5 MB
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    # ATS score thresholds
    ATS_YES_THRESHOLD = 80
    ATS_MAYBE_THRESHOLD = 60
