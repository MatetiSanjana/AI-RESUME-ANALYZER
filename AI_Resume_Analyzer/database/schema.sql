-- schema.sql
-- Defines the two tables used by AI Resume Analyzer.

CREATE TABLE IF NOT EXISTS Resume (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    email TEXT,
    phone TEXT,
    resume_score INTEGER,
    upload_date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER NOT NULL,
    company_name TEXT,
    ats_score INTEGER,
    can_apply TEXT,
    analysis_date TEXT NOT NULL,
    FOREIGN KEY (resume_id) REFERENCES Resume (id)
);
