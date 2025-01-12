"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
debug = DebugToolbarExtension(app)

app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True


app.app_context().push()

connect_db(app)

### User Routes, Hanlding of Posts ####
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
    posts = Post.query.filter_by(user_id=user_id).all()
    for post in posts:
        PostTag.query.filter_by(post_id=post.id).delete()

    Post.query.filter_by(user_id=user_id).delete() # deletes users, posts and commit

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new', methods=["GET"])
def new_post_form(user_id):
    """Show form to add post for user"""
    user = User.query.get_or_404(user_id)
    name = user.full_name()
    tags = Tag.query.order_by(Tag.id).all()

    return render_template('users/new_post.html', id=user_id, name=name, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_new_post(user_id):
    """Create new post"""
    title = request.form['title']
    content = request.form['content']
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    tag_names = request.form.getlist('tags')

    for name in tag_names:
        tag = Tag.query.filter_by(name=name).first()
        if tag:
            post_tag = PostTag(post_id=post.id, tag_id=tag.id)
            db.session.add(post_tag)

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
    print(f"Fething post with ID: {post_id}")
    post = Post.query.get_or_404(post_id)
    print(f"Post fetched: {post}")
    tags = Tag.query.order_by(Tag.id).all()
    print(f"Tags fetched: {tags}")

    return render_template('users/edit_post.html', post=post, tags=tags)

# @app.route('/posts/<int:post_id>/edit', methods=['POST'])
# def edit_post(post_id):
#     """Handle edit post forms"""
#     pr
#     post = Post.query.get_or_404(post_id)
#     post.title = request.form['title']
#     post.content = request.form['content']

#     PostTag.query.filter_by(post_id=post_id).delete()
#     for key in request.form:
#         tag = Tag.query.filter_by(name=key).first()
#         if tag:
#             post_tag = PostTag(post_id=post_id, tag_id=tag.id)
#             db.session.add(post_tag)

#     # Save the changes to the database
#     db.session.add(post)
#     db.session.commit()

#     # Redirect to the post details page
#     return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    print(f"Editing post with ID: {post_id}")
    print(f"Request form data: {request.form}")
    post = Post.query.get_or_404(post_id)

    try:
        post.title = request.form['title']
        post.content = request.form['content']

        PostTag.query.filter_by(post_id=post_id).delete()
        for key in request.form:
            print(f"Processing tag: {key}")
            tag = Tag.query.filter_by(name=key).first()
            if tag:
                post_tag = PostTag(post_id=post_id, tag_id=tag.id)
                db.session.add(post_tag)

        db.session.add(post)
        db.session.commit()
        print("Post edited successfully.")
    except Exception as e:
        print(f"Error editing post: {e}")
        raise e

    return redirect(f'/posts/{post.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete posts"""
    post = Post.query.get_or_404(post_id)
    user_id = post.user.id
    PostTag.query.filter_by(post_id=post_id).delete()
    Post.query.filter_by(post_id=post_id).delete()
                         
    # db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

##### Tag Routes ####


@app.route('/tags')
def show_all_tags():    
    """tag details page"""

    tags = Tag.query.order_by(Tag.id).all()
    return render_template('users/all_tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_posts(tag_id):
    """Show details about a tag with link to edit form and delete"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('users/tag.html', tag=tag)

@app.route('/tags/new')
def new_tag_form():
    """Shows a form to add a tag"""

    return render_template('users/new_tag.html')

@app.route('/tags/new', methods=['POST'])
def create_tag():
    """process add form, adds tag, redirects to tag list"""
    tagname = request.form.get('tagname')
    if not tagname:
        #handle missing input
        flash("Tag name is required!", "error")
    # db.session.add(tag)
    # db.session.commit()
        
        return redirect('/tags/new')
    
    try:
        tag = Tag(name=tagname) 
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error adding tag: {e}") #Log error
        flash("An error occurred when adding the tag.", "error")
        
        return redirect('/tags/new') # Redirect back to the form

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """edit tag page"""
    tag = Tag.query.get_or_404(tag_id)
    
    return render_template('edit_tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    """handle edit tag page"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tagname']
    db.session.add(tag)
    db.session.commit()
    
    return redirect(f'/tags/{tag_id}')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """tag details page"""
    PostTag.query.filter_by(tag_id=tag_id).delete()
    db.session.commit()
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()

    return redirect('/tags')

