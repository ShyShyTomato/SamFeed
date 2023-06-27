from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


"""
This is a many-to-many relationship joing table. It is used to link posts and categories together.
"""
flairs = db.Table('flairs',
                  db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
                  db.Column('flair_id', db.Integer, db.ForeignKey('flair.id'), primary_key=True))
"""
The post class is for posts. It has a many-to-one relationship with the user class. It also has a many-to-many relationship with the flair class.
"""
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user=db.relationship('User', backref='post', lazy=True)
    flairs = db.relationship('Flair', secondary=flairs, lazy='subquery',
                             backref=db.backref('posts', lazy=True))

"""
UserMixin is a class that provides default implementations for the methods that Flask-Login expects user objects to have.
"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=True)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    email = db.Column(db.String, nullable=False, unique=True)
    bio = db.Column(db.String, nullable=True)
    superuser = db.Column(db.Boolean)

"""
This class is for categories. Posts can have multiple categories or no categories.
"""

class Flair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)