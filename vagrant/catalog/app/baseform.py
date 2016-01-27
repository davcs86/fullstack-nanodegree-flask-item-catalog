from . import app
from flask_wtf import Form
from wtforms import HiddenField
from flask import g


class BaseForm(Form):
    # CSRF security based on flask-seasurf
    # https://flask-seasurf.readthedocs.org/en/latest/
    @staticmethod
    @app.before_request
    def add_csrf():
        csrf_name = app.config.get('CSRF_COOKIE_NAME', '_csrf_token')
        setattr(BaseForm,
                csrf_name,
                HiddenField(default=getattr(app, csrf_name, '')))
