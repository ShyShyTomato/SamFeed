from app import db
from flask_login import UserMixin

"""
This is a many-to-many relationship table. It is used to link posts and categories together.
"""
flairs = db.Table('flairs',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('flair_id', db.Integer, db.ForeignKey('flair.id'), primary_key=True)
)

"""
Post class haha funny
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
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)

"""
This class is for categories. Posts can have multiple categories or no categories.
"""

class Flair(db.Model):
    id = db.Column(db.Integer, primary_key=True)