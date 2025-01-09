"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
debug = DebugToolbarExtension(app)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.app_context().push()

connect_db(app)

@app.route('/')
def show_home():
    """Redirect to list of users"""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Show all users"""
    users = User.query.all()
    print(users)
    return render_template('users/users_listing.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_home():
    """Show a form to create a new User"""
    return render_template('users/new_user.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():    
    #  """Handle new user creation with form submission"""
    user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or None
    )
    
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    # """ Show information about specific user """
    user = User.query.get_or_404(user_id)
    return render_template('users/user_details.html', id=user_id, user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    # """ Show edit page for user"""
    user = User.query.get(user_id)
    return render_template('users/edit_user.html', id=user_id, user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edits_user(user_id):
    """ Process edit form """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """ Deletes user """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_post_form(user_id):
    """Show form to add post for user"""
    user = User.query.get_or_404(user_id)
    name = user.full_name()

    return render_template('users/new_post.html', id=user_id, name=name)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    """Create new post"""
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show posts"""
    post = Post.query.get_or_404(post_id)

    return render_template('users/post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show form to edit posts"""
    post = Post.query.get_or_404(post_id)

    return render_template('users/edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handle edit post forms"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    # Save the changes to the database
    db.session.commit()

    # Redirect to the post details page
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete posts"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')