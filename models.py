from flask_sqlalchemy import SQLAlchemy

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
    image_url = db.Column(db.String(150), nullable = False, default='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTArDP_bnVwv1r88E7xDWOt6utBQv1HdPsensjcjjtwfg&s')