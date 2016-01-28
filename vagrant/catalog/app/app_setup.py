from flask import Flask
from sqlalchemy import create_engine
from flask.ext.login import LoginManager
from sqlalchemy.orm import sessionmaker
from .config import DevelopmentConfig as app_config
from flask.ext.seasurf import SeaSurf
from models.base import Base
from models.category import Category
from models.user import User
from models.item import Item
from sqlalchemy_imageattach.stores.fs import HttpExposedFileSystemStore

app = Flask(__name__)
app.config.from_object(app_config)
csrf = SeaSurf()
csrf.init_app(app)
fs_store = HttpExposedFileSystemStore('app/static', 'images/')
app.wsgi_app = fs_store.wsgi_middleware(app.wsgi_app)

engine = create_engine(app_config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

login_manager = LoginManager()
login_manager.init_app(app)
