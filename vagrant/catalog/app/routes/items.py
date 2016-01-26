from .. import app, db_session, OAuthSignIn, User, Item
from flask.ext.login import current_user, login_user, login_required
from flask import flash, redirect, url_for, render_template, request


@app.route('/')
@app.route('/index')
def index():
    page = request.form.get('page', 1)
    filter_query = request.form.get('query', False)
    filter_filterbycat = 'filterbycat' in request.form
    filter_categories = request.form.getlist('categories[]')
    items = db_session.query(Item).all()[(page-1)*10::10]
    if filter_query is not False:
        items = db_session.query(Item) \
            .filter((Item.name.ilike(filter_query)) |
                    (Item.description.ilike(filter_query))) \
            .all()[(page-1)*10::10]
    return render_template('index.html', items=items)


@app.route('/newitem', methods=['GET', 'POST'])
@login_required
def item_new():
    if request.method == 'GET':
        return render_template('item_form.html')
    return 'Item form in POST method'
