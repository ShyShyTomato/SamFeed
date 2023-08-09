from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SelectMultipleField,
                      TextAreaField, IntegerField, SelectField)
from wtforms.validators import DataRequired, Length, Email, InputRequired
from app import db


class loginForm(FlaskForm):
    """Login form lets users login."""
    id = db.Column(db.Integer, primary_key=True)    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class registerForm(FlaskForm):
    """Register form lets users register."""
    id = db.Column(db.Integer, primary_key=True)
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

class postForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    text = StringField('Text', validators=[DataRequired(), Length(max=256)], 
                       render_kw={"placeholder": "Text"})
    flairs = SelectMultipleField('Flairs', choices=[], validators=[DataRequired()], 
                                 render_kw={"placeholder": "Flairs"})

class bioForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    text = TextAreaField('Bio', validators=[DataRequired(), Length(max=256)], 
                         render_kw={"placeholder": "Bio"})

class editForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    text = StringField('Text', validators=[DataRequired(), Length(max=256)], 
                       render_kw={"placeholder": "Text"})
    flairs = SelectMultipleField('Flairs', choices=[],
                                  validators=[DataRequired()], render_kw={"placeholder": "Flairs"})

class sortByForm(FlaskForm):
    userID = IntegerField('userID', validators=[InputRequired()], default=0)
    flairs = SelectField('Flairs', choices=[], 
                         validators=[DataRequired()], render_kw={"placeholder": "Flairs"})
