from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Site user"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String(1500), nullable = False, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTArDP_bnVwv1r88E7xDWOt6utBQv1HdPsensjcjjtwfg&s')

class Post(db.Model):
    """User posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', backref='posts')

    tags = db.relationship('Tag', secondary='post_tags', backref='posts')

class Tag(db.Model):
    """Tags for posts"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)

class PostTag(db.Model):
    """Mapping of posts with tags"""

    __tablename__ = "post_tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))

