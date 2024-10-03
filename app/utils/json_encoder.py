from flask.json.provider import DefaultJSONProvider
from app.models import WorkflowStep

class CustomJSONEncoder(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, WorkflowStep):
            return {
                'id': obj.id,
                'tool_id': obj.tool_id,
                'order': obj.order,
                'arguments': obj.arguments
            }
        return super().default(obj)