from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SelectMultipleField,
                     TextAreaField, IntegerField, SelectField)
from wtforms.validators import DataRequired, Length, Email, InputRequired
from app import db


class LoginForm(FlaskForm):
    """Login form lets users login."""
    id = db.Column(db.Integer, primary_key=True)
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    """Register form lets users register."""
    id = db.Column(db.Integer, primary_key=True)
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])


class PostForm(FlaskForm):
    """Post form lets a user create a post."""
    id = db.Column(db.Integer, primary_key=True)
    text = TextAreaField('Text', validators=[DataRequired(), Length(max=256)],
                         render_kw={"placeholder": "Text"})
    flairs = SelectMultipleField('Flairs', choices=[],
                                 validators=[DataRequired()],
                                 render_kw={"placeholder": "Flairs"})


class BioForm(FlaskForm):
    """Bio form lets a user create a bio."""
    id = db.Column(db.Integer, primary_key=True)
    text = TextAreaField('Bio', validators=[DataRequired(), Length(max=256)],
                         render_kw={"placeholder": "Bio"})


class EditForm(FlaskForm):
    """Edit form lets a user edit a post."""
    id = db.Column(db.Integer, primary_key=True)
    text = TextAreaField('Text', validators=[DataRequired(), Length(max=256)],
                         render_kw={"placeholder": "Text"})
    flairs = SelectMultipleField('Flairs', choices=[],
                                 validators=[DataRequired()],
                                 render_kw={"placeholder": "Flairs"})


class SortByForm(FlaskForm):
    """SortBy form lets a user sort posts by flair."""
    userID = IntegerField('userID', validators=[InputRequired()], default=0)
    flairs = SelectField('Flairs', choices=[],
                         validators=[DataRequired()],
                         render_kw={"placeholder": "Flairs"})
