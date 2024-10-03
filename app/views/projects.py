from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.project import Project
from flask_wtf import FlaskForm
from wtforms import StringField, URLField
from wtforms.validators import DataRequired, URL
from functools import wraps

bp = Blueprint("projects", __name__)

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired()])
    target_url = URLField('Target URL', validators=[DataRequired(), URL()])

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@bp.route("/projects/new", methods=["GET", "POST"])
@login_required
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, target_url=form.target_url.data, user_id=current_user.id)
        db.session.add(project)
        db.session.commit()
        flash("Project created successfully.", "success")
        return redirect(url_for("projects.list_projects"))

    return render_template("projects/new.html", form=form)

@bp.route("/projects")
@login_required
def list_projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template("projects/list.html", projects=projects)

@bp.route("/projects/<int:project_id>")
@login_required
def view_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash("You do not have permission to view this project.", "danger")
        return redirect(url_for("projects.list_projects"))
    return render_template("projects/view.html", project=project)

@bp.route("/admin/projects")
@login_required
@admin_required
def admin_projects():
    projects = Project.query.all()
    return render_template("projects/admin_list.html", projects=projects)
