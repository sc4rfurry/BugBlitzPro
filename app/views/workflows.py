from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db, csrf
from app.models.workflow import Workflow, WorkflowStep
from app.models.project import Project
from app.models.tool import Tool
from app.models.settings import LanguageBinary
from app.tasks.workflow_tasks import execute_workflow
from flask_wtf.csrf import validate_csrf
from wtforms.validators import ValidationError


bp = Blueprint("workflows", __name__)


@bp.route("/projects/<int:project_id>/workflows")
@login_required
def list_workflows(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("projects.list_projects"))

    workflows = Workflow.query.filter_by(project_id=project_id).all()
    return render_template("workflows/list.html", project=project, workflows=workflows)


@bp.route("/projects/<int:project_id>/workflows/new", methods=["GET", "POST"])
@login_required
@csrf.exempt  # Exempt this route from CSRF protection as we'll handle it manually
def create_workflow(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("projects.list_projects"))

    # Fetch tools
    tools = Tool.query.filter(
        (Tool.user_id == current_user.id) | (Tool.is_custom == False)
    ).all()

    # Check if there are any tools available
    if not tools:
        flash("Please add at least one tool before creating a workflow.", "warning")
        return redirect(url_for("tools.create_tool"))

    # Fetch language binaries
    language_binaries = LanguageBinary.query.filter_by(user_id=current_user.id).first()
    
    # If language binaries don't exist, create an empty dictionary
    if not language_binaries:
        language_binaries_data = {
            "python": None,
            "node": None,
            "ruby": None
        }
    else:
        language_binaries_data = {
            "python": language_binaries.python_path,
            "node": language_binaries.node_path,
            "ruby": language_binaries.ruby_path
        }

    if request.method == "POST":
        try:
            validate_csrf(request.json.get("csrf_token"))
        except ValidationError:
            return jsonify({"status": "error", "message": "Invalid CSRF token"}), 400

        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

        name = data.get("name")
        if not name:
            return jsonify({"status": "error", "message": "Workflow name is required"}), 400

        try:
            workflow = Workflow(name=name, project_id=project_id)
            db.session.add(workflow)

            for index, step_data in enumerate(data.get("steps", [])):
                step = WorkflowStep(
                    workflow=workflow,
                    tool_id=step_data.get("tool_id"),
                    order=index,
                    type=step_data.get("type", "tool"),
                    name=step_data.get("name"),
                    path=step_data.get("path"),
                    left=step_data.get("left", 0),
                    top=step_data.get("top", 0),
                )
                db.session.add(step)

            db.session.commit()
            return jsonify({"status": "success", "workflow_id": workflow.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    # Convert tools to a JSON-serializable format
    tools_data = [
        {"id": tool.id, "name": tool.name, "category": tool.category} for tool in tools
    ]

    return render_template(
        "workflows/new.html",
        project=project,
        tools=tools_data,
        language_binaries=language_binaries_data,
    )


@bp.route("/api/tools")
@login_required
def get_tools():
    tools = Tool.query.filter(
        (Tool.user_id == current_user.id) | (Tool.is_custom == False)
    ).all()
    return jsonify([{"id": tool.id, "name": tool.name} for tool in tools])


@bp.route("/workflows/<int:workflow_id>/edit", methods=["GET", "POST"])
@login_required
@csrf.exempt  # Exempt this route from CSRF protection as we'll handle it manually
def edit_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    if workflow.project.user_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("projects.list_projects"))

    if request.method == "POST":
        try:
            validate_csrf(request.json.get("csrf_token"))
        except ValidationError:
            return jsonify({"status": "error", "message": "Invalid CSRF token"}), 400

        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "Invalid data"}), 400

        workflow.name = data.get("name", workflow.name)

        # Get the IDs of steps in the updated workflow
        updated_step_ids = [
            step["id"]
            for step in data.get("steps", [])
            if not isinstance(step["id"], str) or not step["id"].startswith("new-")
        ]

        # Delete steps that are no longer in the workflow
        WorkflowStep.query.filter(
            WorkflowStep.workflow_id == workflow.id,
            ~WorkflowStep.id.in_(updated_step_ids),
        ).delete(synchronize_session=False)

        # Update or create steps
        for index, step_data in enumerate(data.get("steps", [])):
            if isinstance(step_data["id"], str) and step_data["id"].startswith("new-"):
                # Create new step
                step = WorkflowStep(
                    workflow=workflow,
                    tool_id=step_data["tool_id"],  # Changed back to "tool_id"
                    order=index,
                    left=step_data.get("left", 0),
                    top=step_data.get("top", 0),
                )
                db.session.add(step)
            else:
                # Update existing step
                step = WorkflowStep.query.get(step_data["id"])
                if step:
                    step.tool_id = step_data["tool_id"]  # Changed back to "tool_id"
                    step.order = index
                    step.left = step_data.get("left", 0)
                    step.top = step_data.get("top", 0)

        try:
            db.session.commit()
            return jsonify(
                {
                    "status": "success",
                    "steps": [step.to_dict() for step in workflow.steps],
                }
            )
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    tools = Tool.query.filter(
        (Tool.user_id == current_user.id) | (Tool.is_custom == False)
    ).all()

    # Sort the steps by order
    sorted_steps = sorted(workflow.steps, key=lambda step: step.order)

    existing_steps = [
        {
            "id": step.id,
            "tool_id": step.tool_id,
            "name": step.tool.name,  # Add this line
            "category": step.tool.category,  # Add this line
            "order": step.order,
            "left": step.left,
            "top": step.top,
        }
        for step in sorted_steps
    ]

    return render_template(
        "workflows/edit.html",
        workflow=workflow,
        tools=[
            {"id": tool.id, "name": tool.name, "category": tool.category}
            for tool in tools
        ],
        existing_steps=existing_steps,
    )


@bp.route("/workflows/<int:workflow_id>/execute", methods=["POST"])
@login_required
def execute_workflow_route(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    if workflow.project.user_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("projects.list_projects"))

    task = execute_workflow.delay(workflow_id)
    flash("Workflow execution started.", "info")
    return redirect(url_for("workflows.list_workflows", project_id=workflow.project_id))


@bp.route("/workflows/<int:workflow_id>/delete", methods=["POST"])
@login_required
def delete_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    if workflow.project.user_id != current_user.id:
        flash("Access denied.", "danger")
        return redirect(url_for("projects.list_projects"))

    project_id = workflow.project_id
    db.session.delete(workflow)
    db.session.commit()
    flash("Workflow deleted successfully.", "success")
    return redirect(url_for("workflows.list_workflows", project_id=project_id))