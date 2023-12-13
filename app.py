"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Secret!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def list_users():
    """List Users and show button to open form to add user""" 
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new')
def show_add_user_form():    
    """Get new user form"""
    return render_template("newuserform.html")


@app.route('/users/new', methods=["POST"])
def add_user():
    """Add the new user and redirect to the user detail page"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["user-image"]

    new_user = User(first_name=first_name, last_name=last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")

@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show info on a singler user"""
    user = User.query.get_or_404(user_id)
    return render_template("userdetails.html", user=user)

if __name__ == '__main__':
    app.run()