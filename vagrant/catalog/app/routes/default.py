from .. import app, db_session, OAuthSignIn, User
from flask.ext.login import current_user, login_user
from flask import flash, redirect, url_for, render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
