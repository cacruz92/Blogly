"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post


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

# User routes

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

# Post routes


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):    
    """Get new post form"""
    user = User.query.get_or_404(user_id)
    return render_template("newpostform.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """Add the new post and redirect to the user detail page"""
    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user=user)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show info on a singler post"""
    post = Post.query.get_or_404(post_id)
    return render_template("postdetails.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(post_id):
    """Edits existing post."""
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    
    db.session.add(post)
    db.session.commit()

    return redirect("/")

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_edit_user_form(post_id):
    """Populates the form that allows you to edit a particular post"""
    post = Post.query.get_or_404(post_id)
    return render_template("editpost.html", post=post)

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Deletes post from table"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/")

# Tag Routes

@app.route('/tags')
def list_users():
    """Lists all tags, with links to the tag detail page.""" 
    tags = Tag.query.all()
    return render_template("tags.html", tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("showtag.html", tag=tag)

@app.route('/tags/new')
def show_new_tag_form():
    """Shows a form to add a new tag"""
    return render_template("newtagform.html")

@app.route('/tags/new', methods=["POST"])
def show_new_tag_form():
    """Process add form, adds tag, and redirect to tag list"""
    name = request.form["name"]

    new_tag = Tag(name = name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form():
    """Shows a form to edit tag"""
    return render_template("edittag.html")

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def show_edit_tag_form():
    """Process edit form, edit tag, and redirects to the tags list. """
    tag = Post.query.get_or_404(tag_id)
    tag.name = request.form["name"]

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_post(tag_id):
    """Deletes tag from table"""
    tag = Post.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    return redirect("/tags")

if __name__ == '__main__':
    app.run()