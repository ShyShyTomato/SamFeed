from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SamFeed.db'
db = SQLAlchemy(app)

#Grab all the things.
from app import routes, models

#Secret key for session management
app.config['SECRET_KEY'] = 'lol'

#app.app_context().push()