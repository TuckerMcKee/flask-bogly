"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
# ***************************************change to 'postgresql:///blogly' for main app, this db is for testing
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.debug = True
# debug = DebugToolbarExtension(app)

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
    return render_template('userdetail.html',user=db.session.get(User, user_id),posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """display form for editing user data"""
    return render_template('edituser.html',user=db.session.get(User, user_id))

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def update_user_data(user_id):
    """update user data with form data and redirect to user list"""
    user = db.session.get(User, user_id)
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
    user = db.session.get(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """show form for new post creation"""
    user = db.session.get(User, user_id)
    return render_template('addpost.html',user=user)

@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def create_new_post(user_id):
    """process data for new post and redirect to user detail page"""
    user = db.session.get(User, user_id)
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title,content=content,user_id=user_id)
    db.session.add(new_post)
    tag_ids = request.form.getlist('tags')
    if tag_ids:
        for tag_id in tag_ids:
            new_post_tag = PostTag(tag_id=tag_id,post_id=new_post.id)
            db.session.add(new_post_tag)  
    db.session.commit()
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('userdetail.html',user=user,posts=posts)

@app.route('/posts/<int:post_id>')
def post_detail(post_id):
    """display post detail"""
    post = db.session.get(Post, post_id)
    tags = db.session.query(Tag).join(PostTag).filter(PostTag.post_id == post_id).all() 
    return render_template('postdetail.html',post=post, user=db.session.get(User, post.user_id), tags=tags)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """display form for editing post data"""
    tags = Tag.query.all()
    return render_template('editpost.html',post=db.session.get(Post, post_id), tags=tags)

@app.route('/posts/<int:post_id>/edit', methods = ["POST"])
def update_post_data(post_id):
    """update post data with form data and redirect to post detail"""
    post = db.session.get(Post, post_id)
    new_title = request.form['title']
    new_content = request.form['content']
    tag_ids = request.form.getlist('tags')
    if new_title:
        post.title = new_title
    if new_content:
        post.content = new_content 
    if tag_ids:
        for tag_id in tag_ids:
            new_post_tag = PostTag(tag_id=tag_id,post_id=post_id)
            db.session.add(new_post_tag) 
    tags = db.session.query(Tag).join(PostTag).filter(PostTag.post_id == post_id).all()           
    db.session.commit()      
    return render_template('postdetail.html',post=post, user=db.session.get(User, post.user_id),tags=tags)

@app.route('/posts/<int:post_id>/delete', methods = ["POST"])
def delete_post_data(post_id):
    """delete post data and redirect to user list"""
    post = db.session.get(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/users')

@app.route('/tags')
def show_tags():
    """display list of all tags"""
    return render_template('taglist.html',tags=Tag.query.all())

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """display tag detail"""
    posts = db.session.query(Post).join(PostTag).filter(PostTag.tag_id == tag_id).all()
    return render_template('tagdetail.html',tag=db.session.get(Tag, tag_id),posts=posts)

@app.route('/tags/new')
def new_tag_form():
    """show form for new tag creation"""
    return render_template('addtag.html')

@app.route('/tags/new', methods = ["POST"])
def create_new_tag():
    """process new tag data and redirect to tag list"""
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_form(tag_id):
    """display form for editing tag data"""
    return render_template('edittag.html', tag=db.session.get(Tag,tag_id))

@app.route('/tags/<int:tag_id>/edit', methods = ["POST"])
def update_tag_data(tag_id):
    """update tag data with form data and redirect to tag list"""
    tag = db.session.get(Tag,tag_id)
    edit_name = request.form['name']
    if edit_name:    
        tag.name = edit_name
    db.session.commit()      
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods = ["POST"])
def delete_tag_data(tag_id):
    """delete tag data and redirect to tag list"""
    post_tags = db.session.query(Post).filter(PostTag.tag_id == tag_id).all()
    for post_tag in post_tags:
        db.session.delete(post_tag)
    tag = db.session.get(Tag, tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')


