from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db, csrf
from app.models.tool import Tool

bp = Blueprint("tools", __name__)

@bp.route("/tools")
@login_required
def list_tools():
    tools = Tool.query.filter(
        (Tool.user_id == current_user.id) | (Tool.is_custom == False)
    ).all()
    return render_template("tools/list.html", tools=tools)

@bp.route("/tools/new", methods=["GET", "POST"])
@login_required
def create_tool():
    if request.method == "POST":
        name = request.form["name"]
        command = request.form["command"]
        category = request.form["category"]
        description = request.form["description"]

        tool = Tool(
            name=name,
            command=command,
            category=category,
            description=description,
            is_custom=True,
            user_id=current_user.id,
        )
        db.session.add(tool)
        db.session.commit()

        flash("Tool created successfully.", "success")
        return redirect(url_for("tools.list_tools"))

    return render_template("tools/new.html")

@bp.route("/tools/<int:tool_id>")
@login_required
def view_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    if tool.user_id != current_user.id and tool.is_custom:
        flash("You do not have permission to view this tool.", "danger")
        return redirect(url_for("tools.list_tools"))
    return render_template("tools/view.html", tool=tool)

@bp.route("/tools/<int:tool_id>/edit", methods=["GET", "POST"])
@login_required
def edit_tool(tool_id):
    tool = Tool.query.get_or_404(tool_id)
    if tool.user_id != current_user.id:
        flash("You do not have permission to edit this tool.", "danger")
        return redirect(url_for("tools.list_tools"))

    if request.method == "POST":
        tool.name = request.form["name"]
        tool.command = request.form["command"]
        tool.category = request.form["category"]
        tool.description = request.form["description"]

        db.session.commit()
        flash("Tool updated successfully.", "success")
        return redirect(url_for("tools.view_tool", tool_id=tool.id))

    return render_template("tools/edit.html", tool=tool)
