from app import db

class Tool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    command = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    is_custom = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('tools', lazy=True))

    def __repr__(self):
        return f'<Tool {self.name}>'