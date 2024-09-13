"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return redirect('/users')

@app.route('/users')
def show_users():
    """display list of all users"""
    return render_template('userlisting.html',users=User.query.all())

@app.route('/users/new')
def new_user_form():
    """show form for new user creation"""
    return render_template('newuser.html')

@app.route('/users/new', methods = ["POST"])
def create_new_user():
    """process new user data and redirect to user list"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """display user detail"""
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('userdetail.html',user=User.query.get(user_id),posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """display form for editing user data"""
    return render_template('edituser.html',user=User.query.get(user_id))

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def update_user_data(user_id):
    """update user data with form data and redirect to user list"""
    user = User.query.get(user_id)
    new_first_name = request.form['first_name']
    new_last_name = request.form['last_name']
    new_image_url = request.form['image_url']
    if new_first_name:
        user.first_name = new_first_name
    if new_last_name:
        user.last_name = new_last_name 
    if new_image_url:
        user.image_url = new_image_url
    db.session.commit()      
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user_data(user_id):
    """delete user data and redirect to user list"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """show form for new post creation"""
    user = User.query.get(user_id)
    return render_template('addpost.html',user=user)

@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def create_new_post(user_id):
    """process data for new post and redirect to user detail page"""
    user = User.query.get(user_id)
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title,content=content,user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return render_template('userdetail.html',user=User.query.get(user_id))

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    """display post detail"""
    post = Post.query.get(post_id)
    return render_template('postdetail.html',post=post, user=User.query.get(post.user_id))

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """display form for editing post data"""
    return render_template('editpost.html',post=Post.query.get(post_id))

@app.route('/posts/<int:post_id>/edit', methods = ["POST"])
def update_post_data(post_id):
    """update post data with form data and redirect to post detail"""
    post = Post.query.get(post_id)
    new_title = request.form['title']
    new_content = request.form['content']
    if new_title:
        post.title = new_title
    if new_content:
        post.content = new_content 
    db.session.commit()      
    return render_template('postdetail.html',post=post, user=User.query.get(post.user_id))

@app.route('/posts/<int:post_id>/delete', methods = ["POST"])
def delete_post_data(post_id):
    """delete post data and redirect to user list"""
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')








