from .. import app, db_session, OAuthSignIn, User
from flask.ext.login import current_user, login_user, login_required
from flask import flash, redirect, url_for
from passlib.hash import sha256_crypt


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/unlink/<provider>')
@login_required
def oauth_unlink(provider):
    user = current_user
    if provider == 'google':
        user.google_id = ''
    elif provider == 'facebook':
        user.facebook_id = ''
    elif provider == 'twitter':
        user.twitter_id = ''
    elif provider == 'github':
        user.github_id = ''
    db_session.add(user)
    db_session.commit()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    oauth = OAuthSignIn.get_provider(provider)
    social_id, nickname = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    if current_user.is_authenticated:
        user = current_user
        redirect_to = 'me'
    else:
        user = db_session.query(User) \
                .filter((User.google_id == social_id) |
                        (User.facebook_id == social_id) |
                        (User.twitter_id == social_id) |
                        (User.github_id == social_id)) \
                .first()
        redirect_to = 'index'
        if user is None:
            # New user, register and send it to profile page
            user = User(nickname=nickname)
            user.password = sha256_crypt.encrypt('')
            redirect_to = 'me'
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
