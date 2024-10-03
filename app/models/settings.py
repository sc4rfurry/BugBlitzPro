from app import db

class LanguageBinary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    python_path = db.Column(db.String(255))
    node_path = db.Column(db.String(255))
    ruby_path = db.Column(db.String(255))

    user = db.relationship('User', backref=db.backref('language_binaries', lazy=True))

    def __repr__(self):
        return f'<LanguageBinary {self.id}>'