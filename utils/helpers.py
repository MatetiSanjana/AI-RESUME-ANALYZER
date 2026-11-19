"""
helpers.py
----------
Miscellaneous small helper functions shared across the app.
"""

from datetime import datetime


def current_timestamp():
    """Return current date-time as a readable string for DB storage."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def safe_get(dictionary, key, default=""):
    """Safely fetch a key from a dict, returning a default if missing."""
    if not isinstance(dictionary, dict):
        return default
    return dictionary.get(key, default) or default
