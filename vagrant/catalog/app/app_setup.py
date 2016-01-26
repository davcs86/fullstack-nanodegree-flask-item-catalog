from flask import Flask
from sqlalchemy import create_engine
from flask.ext.login import LoginManager
from sqlalchemy.orm import sessionmaker
from .config import DevelopmentConfig as app_config
from models.base import Base
from models.category import Category
from models.user import User
from models.item import Item

app = Flask(__name__)
app.config.from_object(app_config)

engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

login_manager = LoginManager()
login_manager.init_app(app)
