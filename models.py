"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        return f"<user id={self.id} first_name={self.first_name} last_name={self.last_name} image_url={self.image_url}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False,unique=True)
    last_name = db.Column(db.String(20),unique=True)
    image_url = db.Column(db.String, default='https://winaero.com/blog/wp-content/uploads/2018/08/Windows-10-user-icon-big.png', nullable=False)

    def __init__(self, first_name, last_name, image_url=None):
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url or 'https://winaero.com/blog/wp-content/uploads/2018/08/Windows-10-user-icon-big.png'

    # posts = db.relationship('Post')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.String(40), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete= 'CASCADE'), nullable=False)

    user = db.relationship('User', backref='posts')

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String(20), unique=True, nullable=False) 

    post_tag = db.relationship('PostTag', backref='tags', passive_deletes=True)  

class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id',ondelete= 'CASCADE'), primary_key=True) 
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id',ondelete= 'CASCADE'), primary_key=True)  

    tag = db.relationship('Tag', backref='post_tags')      
