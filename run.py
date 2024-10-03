from app import create_app, db
from app.models import User, Project, Tool, Workflow, WorkflowStep

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Project': Project, 'Tool': Tool, 'Workflow': Workflow, 'WorkflowStep': WorkflowStep}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
