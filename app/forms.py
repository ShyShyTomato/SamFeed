from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from app import db

# Login form
class loginForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)    
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

# Register form
class RegisterForm(FlaskForm):
    id = db.Column(db.Integer, primary_key=True)
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])