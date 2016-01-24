from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from .config import DevelopmentConfig as app_config

app = Flask(__name__)
app.config.from_object(app_config)
db = SQLAlchemy(app)

from models import User

db.create_all()

from routes import default
