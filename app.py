"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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
    return render_template('userdetail.html',user=User.query.get(user_id))

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






