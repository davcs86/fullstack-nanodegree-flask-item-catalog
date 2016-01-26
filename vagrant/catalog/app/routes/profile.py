from .. import app, db_session, OAuthSignIn, User, login_manager
from flask.ext.login import current_user, login_user, logout_user, \
                            login_required
from flask import flash, redirect, url_for, render_template, request
from passlib.hash import sha256_crypt


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return db_session.query(User).filter_by(id=int(id)).first()


@app.route('/me', methods=['GET', 'POST'])
@login_required
def me():
    if request.method == 'GET':
        return render_template('profile.html')
    success = False
    user = current_user
    pwd = request.form['current_password']
    newpassword = request.form['new_password']
    conpassword = request.form['confirm_password']
    if user is None:
        flash("Session expired")
    elif user.password != '' and not sha256_crypt.verify(pwd, user.password):
        flash("Wrong password")
    elif (user.password == '' or
            (user.password != '' and
             sha256_crypt.verify(pwd, user.password))):
        if len(newpassword) < 6:
            flash("Your new password must be longer than 6 characters")
        elif newpassword != conpassword:
            flash("Password confirmation doesn't match")
        else:
            flash("Password changed successfully")
            success = True
            user.password = sha256_crypt.encrypt(newpassword)
            db_session.add(user)
            db_session.commit()
    else:
        flash("Unknown error")
    return render_template('profile.html', is_success=success)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html')
    # Process login
    nickname = request.form['username']
    password = request.form['password']
    user = db_session.query(User).filter_by(nickname=nickname).first()
    if user is None:
        flash("User not found")
        return render_template('login.html')
    elif user.password == '':
        flash("Your account has no password associated. If you registered ",
              "with a social service, please login with it and set a password")
        return render_template('login.html', usr=nickname)
    elif sha256_crypt.verify(password, user.password):
        login_user(user)
        return redirect(url_for('index'))
    else:
        flash("Wrong password")
        return render_template('login.html', usr=nickname)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('login.html', is_register=True)
    # Process login
    nickname = request.form['username']
    password = request.form['password']
    user = db_session.query(User).filter_by(nickname=nickname).first()
    if user is not None:
        flash("Username is already registered")
        return render_template('login.html', is_register=True, usr=nickname)
    elif len(nickname) < 6:
        flash("Your username must be longer than 6 characters")
        return render_template('login.html', is_register=True, usr=nickname)
    elif len(password) < 6:
        flash("Your password must be longer than 6 characters")
        return render_template('login.html',
                               is_register=True,
                               usr=nickname,
                               pwd=password)
    else:
        user = User(nickname=nickname)
        user.password = sha256_crypt.encrypt(password)
        db_session.add(user)
        db_session.commit()
        login_user(user)
        return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
