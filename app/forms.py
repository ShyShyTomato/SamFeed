from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from app import db

"""Login form lets users login."""
class loginForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

"""Register form lets users register."""
class RegisterForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])