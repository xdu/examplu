from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entry_id = db.Column(db.String, nullable=False)
    examples = db.relationship('Example', backref='entry', lazy=True)

    def __repr__(self):
        return f'<Entry {self.id}: {self.entry_id}>'

class Example(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    mark = db.Column(db.Integer, nullable=True)
    end = db.Column(db.Integer, nullable=True)
    audio_file = db.Column(db.String, nullable=True)
    entry_id = db.Column(db.Integer, db.ForeignKey('entry.id'), nullable=False)

    def __repr__(self):
        return f'<Example {self.id}: {self.text[:50]}>'

class Comprehension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(200), nullable=False)
    created_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comprehension('{self.title}', ' {self.created_time}')"