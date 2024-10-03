from app import db
from datetime import datetime

class Workflow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='created')
    
    project = db.relationship('Project', back_populates='workflows')
    steps = db.relationship('WorkflowStep', back_populates='workflow', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Workflow {self.name}>'

class WorkflowStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workflow_id = db.Column(db.Integer, db.ForeignKey('workflow.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('tool.id'), nullable=True)
    order = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'tool' or 'language'
    name = db.Column(db.String(100), nullable=True)
    path = db.Column(db.String(500), nullable=True)
    arguments = db.Column(db.String(500))
    left = db.Column(db.Integer, default=50)
    top = db.Column(db.Integer, default=50)
    
    workflow = db.relationship('Workflow', back_populates='steps')
    tool = db.relationship('Tool')

    def __repr__(self):
        return f'<WorkflowStep {self.id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "tool_id": self.tool_id,
            "name": self.name or (self.tool.name if self.tool else None),
            "type": self.type,
            "path": self.path,
            "category": self.tool.category if self.tool else None,
            "order": self.order,
            "left": self.left,
            "top": self.top
        }