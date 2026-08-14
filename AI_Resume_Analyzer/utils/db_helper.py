"""
db_helper.py
------------
Small wrapper around SQLite so the rest of the app never
writes raw connection-handling code. Provides:
- init_db(): creates tables from schema.sql if not present
- get_connection(): returns a sqlite3 connection
- insert_resume() / insert_analysis(): simple insert helpers
"""

import sqlite3
import os
from config import Config


def get_connection():
    """Return a new SQLite connection with row access by column name."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the database file and tables if they don't already exist."""
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    schema_path = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")

    conn = get_connection()
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()


def insert_resume(candidate_name, email, phone, resume_score, upload_date):
    """Insert a new resume record and return its generated id."""
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO Resume (candidate_name, email, phone, resume_score, upload_date)
           VALUES (?, ?, ?, ?, ?)""",
        (candidate_name, email, phone, resume_score, upload_date),
    )
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return resume_id


def insert_analysis(resume_id, company_name, ats_score, can_apply, analysis_date):
    """Insert a new analysis record linked to a resume."""
    conn = get_connection()
    conn.execute(
        """INSERT INTO Analysis (resume_id, company_name, ats_score, can_apply, analysis_date)
           VALUES (?, ?, ?, ?, ?)""",
        (resume_id, company_name, ats_score, can_apply, analysis_date),
    )
    conn.commit()
    conn.close()


def get_resume_by_id(resume_id):
    """Fetch a single resume record by id."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM Resume WHERE id = ?", (resume_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
