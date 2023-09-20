"""This is the models file for SamFeed."""


from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Flairs is a table that has a many-to-many relationship with posts.
flairs = db.Table('flairs',
                  db.Column('post_id', db.Integer,
                            db.ForeignKey('post.id'), primary_key=True),
                  db.Column('flair_id', db.Integer,
                            db.ForeignKey('flair.id'), primary_key=True))


class Post(db.Model):
    """
    The post class is for posts.

    It has a many-to-one relationship with the user class.
    It also has a many-to-many relationship with the flair class.
    """

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='post', lazy=True)
    flairs = db.relationship('Flair', secondary=flairs, lazy='subquery',
                             backref=db.backref('posts', lazy=True))


class User(db.Model, UserMixin):
    """
    UserMixin is a class that provides default implementations,
    for the methods that Flask-Login expects user objects to have.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=True)

    def set_password(self, password):
        """Hashes the password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Checks the password."""
        return check_password_hash(self.password, password)
    email = db.Column(db.String, nullable=False, unique=True)
    bio = db.Column(db.String, nullable=True)
    superuser = db.Column(db.Boolean)


class Flair(db.Model):
    """
    This class is for categories.
    Posts can have multiple categories or no categories.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
