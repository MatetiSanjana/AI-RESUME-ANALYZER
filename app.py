"""
app.py
------
Entry point of the AI Resume Analyzer Flask application.
Creates the app, applies config, initializes the database,
and registers all blueprints (routes).
"""

from flask import Flask
from config import Config
from utils.db_helper import init_db
from routes.main_routes import main_bp
from routes.analyze_routes import analyze_bp
from routes.result_routes import result_bp
import google.generativeai as genai


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize SQLite database (creates tables if they don't exist)
    init_db()

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(analyze_bp)
    app.register_blueprint(result_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
