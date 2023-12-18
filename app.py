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
def show_homepage():
    """redirects to users page""" 
    return redirect("/users")

@app.route('/users')
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

@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Populates the form that allows you to edit a particular user"""
    user = User.query.get_or_404(user_id)
    return render_template("edituser.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Edits existing user."""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["user-image"]
    db.session.commit()

    return redirect("/")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Deletes user from table"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run()