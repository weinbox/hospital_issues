from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default='بلاغ عن عطل', nullable=False)  # إضافة حقل العنوان مع قيمة افتراضية
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reporter_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='جديد')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(hours=3))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(hours=3), onupdate=lambda: datetime.now() + timedelta(hours=3))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'location': self.location,
            'description': self.description,
            'reporter_name': self.reporter_name,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now() + timedelta(hours=3))
    
    # العلاقات
    issue = db.relationship('Issue', backref='comments')
