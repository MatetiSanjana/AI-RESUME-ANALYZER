# AI Resume Analyzer

A Flask web app that analyzes a resume, optionally compares it against a
job description, and returns a Resume Score, ATS Score, and AI-generated
improvement suggestions (via Google Gemini).

## Tech Stack
Python, Flask, SQLite, HTML, CSS, JavaScript, Bootstrap, Google Gemini API.

## How It Works (architecture in one paragraph)
Python does all the deterministic work: reading PDF/DOCX files
(`services/pdf_reader.py`, `services/docx_reader.py`), calculating the ATS
score by comparing resume skills against job-description skills
(`services/ats_service.py`), and saving results to SQLite
(`utils/db_helper.py`). Gemini is used **only** for language tasks it's
actually good at: turning messy resume text into structured JSON, pulling
skills out of a job description, and writing human-readable feedback
(`services/gemini_service.py`). Gemini never calculates scores — that logic
stays in plain Python so it's transparent and easy to explain.

## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and add your Gemini API key:
   ```bash
   cp .env.example .env
   ```
   Get a free key at https://aistudio.google.com/app/apikey

3. Run the app:
   ```bash
   python app.py
   ```
   Visit http://127.0.0.1:5000

The SQLite database and its two tables (`Resume`, `Analysis`) are created
automatically on first run — no manual migration step needed.

## Project Flow

1. `/` – Home page
2. `/upload` – Upload resume (PDF/DOCX) + optional job description
3. `/analyze` (POST) – Parses resume, extracts JD skills, calculates ATS
   score, generates Gemini feedback, saves a summary to SQLite
4. `/result` – Shows Resume Score, ATS Score, matched/missing skills, and
   AI feedback
5. `/download-report` – Generates and downloads a PDF summary

## Folder Structure

```
AI_Resume_Analyzer/
├── app.py                  # Flask entry point
├── config.py                # Centralized settings
├── database/schema.sql      # Resume + Analysis tables
├── routes/                  # Blueprints (main, analyze, result)
├── services/                 # One responsibility per file
│   ├── pdf_reader.py         # PDF -> text
│   ├── docx_reader.py        # DOCX -> text
│   ├── resume_parser.py      # text -> structured data (via Gemini)
│   ├── ats_service.py        # ATS score math (pure Python)
│   ├── gemini_service.py     # all Gemini API calls
│   └── report_service.py     # PDF report generation
├── utils/                    # db_helper, file_validator, helpers
├── templates/                 # Jinja2 + Bootstrap pages
└── static/                    # css, js
```

## ATS Score Formula (for interview explanation)

```
ATS Score = (Matched Skills / Total JD Skills) x 100 + small bonus points
            (for having contact info, education, experience, projects)

80-100 -> Can Apply: YES
60-79  -> Can Apply: MAYBE
< 60   -> Can Apply: NO
```

## Notes
- Results are held in the Flask session between `/analyze` and `/result`,
  since this is a single-user demo app (no login system, kept simple on
  purpose per project scope).
- Max upload size: 5MB. Allowed types: `.pdf`, `.docx`.
