"""
main_routes.py
---------------
Blueprint for simple page routes: Home and Upload form.
No heavy logic here - just rendering templates.
"""

from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Landing page with project intro and a link to start."""
    return render_template("home.html")


@main_bp.route("/upload")
def upload_page():
    """Show the resume upload form (resume file + optional JD)."""
    return render_template("upload.html")
