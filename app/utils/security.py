import secrets
from flask import session


def generate_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(16)
    return session["csrf_token"]


def validate_csrf_token(token):
    return token == session.get("csrf_token")
