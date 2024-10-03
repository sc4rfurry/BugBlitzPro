from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.settings import LanguageBinary
from app.models.user import User
from werkzeug.utils import secure_filename
import os

bp = Blueprint("settings", __name__)

@bp.route("/settings", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.get(current_user.id)

        if username and username != user.username:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already exists", "error")
            else:
                user.username = username

        if email and email != user.email:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already exists", "error")
            else:
                user.email = email

        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.password = new_password
                    flash("Password updated successfully", "success")
                else:
                    flash("New passwords do not match", "error")
            else:
                flash("Current password is incorrect", "error")

        db.session.commit()
        flash("Settings updated successfully", "success")
        return redirect(url_for("settings.index"))

    return render_template("settings/index.html")

@bp.route("/settings/language_binaries", methods=["GET", "POST"])
@login_required
def language_binaries():
    language_binary = LanguageBinary.query.filter_by(user_id=current_user.id).first()
    if not language_binary:
        language_binary = LanguageBinary(user_id=current_user.id)
        db.session.add(language_binary)

    if request.method == "POST":
        language_binary.python_path = request.form.get("python_path")
        language_binary.node_path = request.form.get("node_path")
        language_binary.ruby_path = request.form.get("ruby_path")
        
        db.session.commit()
        flash("Language binary settings saved successfully", "success")
        return redirect(url_for("settings.language_binaries"))

    return render_template("settings/language_binaries.html", language_binary=language_binary)

@bp.route("/settings/browse_binary", methods=["POST"])
@login_required
def browse_binary():
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.path.expanduser('~'), '.bugblitzpro', 'binaries', filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        return jsonify({"status": "success", "path": file_path})
    return jsonify({"status": "error", "message": "No file provided"}), 400