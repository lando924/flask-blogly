"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
    return render_template('users_listing.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_home():
    """Show a form to create a new User"""
    return render_template('users/new.html')

@app.route('/users/new', methods=["POST"])
def add_new_user():    
    #  """Handle new user creation with form submission"""
    user = User(
        first = request.form['first'],
        last = request.form['last'],
        image = request.form['image'] or None
    )
    
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    # """ Show information about specific user """
    user = User.query.get(user_id)
    return render_template('user_details.html', id=user_id, user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    # """ Show edit page for user"""
    user = User.query.get(user_id)
    return render_template('edit_user.html', id=user_id, user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edits_user(user_id):
    """ Process edit form """
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['url']
    
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