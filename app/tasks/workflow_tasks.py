from app import celery, db
from app.models.workflow import Workflow, WorkflowStep
import subprocess
import shlex
import sys

@celery.task
def execute_workflow(workflow_id):
    workflow = Workflow.query.get(workflow_id)
    if not workflow:
        return {'status': 'error', 'message': 'Workflow not found'}

    # Add your workflow execution logic here
    # ...

    return {'status': 'success', 'message': 'Workflow executed successfully'}

def execute_step(step):
    tool = step.tool
    command = f"{tool.command} {step.arguments}".strip()
    try:
        if sys.platform.startswith('win'):
            process = subprocess.run(command, capture_output=True, text=True, timeout=300, shell=True)
        else:
            process = subprocess.run(shlex.split(command), capture_output=True, text=True, timeout=300)
        return {
            'status': 'success',
            'command': command,
            'stdout': process.stdout,
            'stderr': process.stderr,
            'return_code': process.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'status': 'error',
            'command': command,
            'message': 'Command execution timed out'
        }
    except Exception as e:
        return {
            'status': 'error',
            'command': command,
            'message': str(e)
        }