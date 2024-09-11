"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
    image_url = db.Column(db.String, default='https://winaero.com/blog/wp-content/uploads/2018/08/Windows-10-user-icon-big.png')
