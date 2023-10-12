from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SamFeed.db'
db = SQLAlchemy(app)

# Grab all the things.
from app import routes, models
# Generate a secret key for session management
secret_key = secrets.token_hex(16)

# Secret key for session management
app.config['SECRET_KEY'] = secret_key
# app.app_context().push()
