from app import db
from flask_login import UserMixin


"""
Post class haha funny
"""
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user=db.relationship('User', backref='post', lazy=True)
    categoryID = db.Column(db.Integer, db.ForeignKey('category.id'))

"""
UserMixin is a class that provides default implementations for the methods that Flask-Login expects user objects to have.
"""
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

"""
This class is for categories. Posts can have multiple categories or no categories.
"""

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref='category', lazy=True)