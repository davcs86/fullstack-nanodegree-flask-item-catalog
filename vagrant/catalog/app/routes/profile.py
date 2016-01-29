from .. import *
from passlib.hash import sha256_crypt


class LoginForm(BaseForm):
    nickname = StringField('Username',
                           validators=[
                            DataRequired(),
                            Length(min=6, max=24,
                                   message="Wrong username")
                            ])
    password = PasswordField('Password',
                             validators=[
                              DataRequired(),
                              Length(min=6, max=24,
                                     message="Wrong password")
                              ])


class RegisterForm(BaseForm):
    nickname = StringField('Username',
                           validators=[
                            DataRequired(),
                            Length(min=6, max=24,
                                   message="Username must have between " +
                                           " %(min)d and %(max)d characters")
                            ])
    password = PasswordField('Password',
                             validators=[
                              DataRequired(),
                              Length(min=6, max=24,
                                     message="Password must have between " +
                                             "%(min)d and %(max)d characters"),
                              EqualTo('confirm_password',
                                      message="Passwords doesn't match")
                              ])
    confirm_password = PasswordField('Password confirmation')


class ProfileForm(BaseForm):
    # Current password can be None, when user registered thru oauth
    password = PasswordField('Password')
    new_password = \
        PasswordField('New password',
                      validators=[
                       DataRequired(),
                       Length(min=6, max=24,
                              message="New password must have between " +
                                      "%(min)d and %(max)d characters"),
                       EqualTo('confirm_password',
                               message="Passwords doesn't match")
                      ])
    confirm_password = PasswordField('Password confirmation')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(id):
    return db_session.query(User).filter_by(id=int(id)).first()


@app.route('/me', methods=['GET', 'POST'])
@login_required
def me():
    success = False
    user = current_user
    # WTF Form to handle the submitted data
    form = ProfileForm(request.form)
    if request.method == 'POST' and form.validate():
        userdata = User()
        form.populate_obj(userdata)
        if user is None:
            flash("Session expired")
            return redirect(url_for('login'))
        elif sha256_crypt.verify(userdata.password, user.password):
            flash("Password changed successfully")
            success = True
            user.password = sha256_crypt.encrypt(userdata.new_password)
            db_session.add(user)
            db_session.commit()
        else:
            flash("Wrong password")
    flash_errors(form)
    return render_template('profile.html', form=form, is_success=success)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Disallow this view to logged in users
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # WTF Form to handle the submitted data
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        userdata = User()
        form.populate_obj(userdata)
        user = db_session.query(User) \
                         .filter_by(nickname=userdata.nickname) \
                         .first()
        if user is None:
            flash("Wrong username")
        elif sha256_crypt.verify(userdata.password, user.password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash("Wrong password")
    flash_errors(form)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Disallow this view to logged in users
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # WTF Form to handle the submitted data
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        userdata = User()
        form.populate_obj(userdata)
        user = db_session.query(User) \
                         .filter_by(nickname=userdata.nickname) \
                         .first()
        if user is not None:
            flash("Username is already registered")
        else:
            userdata.password = sha256_crypt.encrypt(userdata.password)
            db_session.add(userdata)
            db_session.commit()
            login_user(userdata)
            return redirect(url_for('index'))
    flash_errors(form)
    return render_template('login.html', is_register=True, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
