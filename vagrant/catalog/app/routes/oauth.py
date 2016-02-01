from .. import *
import time
from passlib.hash import sha256_crypt
# OAuth login is based on Miguel Grinberg's article:
# http://blog.miguelgrinberg.com/post/oauth-authentication-with-flask


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # redirect to the social service
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/unlink/<provider>')
@login_required
def oauth_unlink(provider):
    # unlink the user account to that social service
    user = current_user
    if provider == 'google':
        user.google_id = None
    elif provider == 'twitter':
        user.twitter_id = None
    elif provider == 'github':
        user.github_id = None
    db_session.add(user)
    db_session.commit()
    return redirect(url_for('me'))


@app.route('/callback/<provider>')
def oauth_callback(provider):
    # Receive the callback from the social service
    oauth = OAuthSignIn.get_provider(provider)
    social_id, nickname = oauth.callback()
    if social_id is None:
        # if the social service callback failed, return to index
        flash('Authentication failed.')
        return redirect(url_for('index'))
    if current_user.is_authenticated:
        # if the user is already logged in, link the social login to
        # his/her account and the redirect to profile
        user = current_user
        redirect_to = 'me'
    else:
        # if the user is not already logged in, check if it's associated
        # to an existing account, otherwise, create the user
        user = db_session.query(User) \
                .filter((User.google_id == social_id) |
                        (User.twitter_id == social_id) |
                        (User.github_id == social_id)) \
                .first()
        redirect_to = 'index'
        if user is None:
            # New user, register and send it to profile page
            user = User(nickname=nickname+'_'+str(time.time()*1000))
            # Leave the password empty
            user.password = sha256_crypt.encrypt('')
            redirect_to = 'me'
    if provider == 'google':
        user.google_id = social_id
    elif provider == 'twitter':
        user.twitter_id = social_id
    elif provider == 'github':
        user.github_id = social_id
    db_session.add(user)
    db_session.commit()
    login_user(user, True)
    return redirect(url_for(redirect_to))
