from .. import app, db_session, OAuthSignIn, User
from flask.ext.login import current_user, login_user
from flask import flash, redirect, url_for


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_id, nickname, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    if not current_user.is_anonymous:
        user = current_user
        redirect_to = 'index'
    else:
        user = db_session.query(User).filter_by(nickname=nickname).one()
        if user is None:
            user = User(nickname=nickname, email=email)
        redirect_to = 'index'
    if provider == 'google':
        user.google_id = social_id
    elif provider == 'facebook':
        user.facebook_id = social_id
    elif provider == 'twitter':
        user.twitter_id = social_id
    elif provider == 'github':
        user.github_id = social_id
    db_session.add(user)
    db_session.commit()
    login_user(user, True)
    return redirect(url_for(redirect_to))
