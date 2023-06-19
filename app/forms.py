from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length, Email
from app import db

"""Login form lets users login."""

class loginForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

"""Register form lets users register."""

class registerForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

class postForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    text = StringField('Text', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "Text"})
    # Try this stuff
    # https://stackoverflow.com/questions/70563907/display-wtforms-selectmultiplefield-display-as-drop-down-and-not-list
    # https://stackoverflow.com/questions/19206919/how-to-create-checkbox-inside-dropdown
    flairs = SelectMultipleField('Flairs', choices=[], validators=[DataRequired()], render_kw={"placeholder": "Flairs"})

class bioForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    text = TextAreaField('Bio', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "Bio"})

class editForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    text = StringField('Text', validators=[DataRequired(), Length(max=256)], render_kw={"placeholder": "Text"})
    flairs = SelectMultipleField('Flairs', choices=[], validators=[DataRequired()], render_kw={"placeholder": "Flairs"})