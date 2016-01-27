from .. import app, db_session, OAuthSignIn, \
               Item, Category, login_manager, BaseForm, \
               flash_errors, OpenSelectMultipleField, \
               slugify_category_list
from flask.ext.login import current_user, login_user, login_required
from flask import flash, redirect, url_for, render_template, request
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask.ext.uploads import UploadSet, IMAGES

allowed_uploads = UploadSet('images', IMAGES)


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


class AddItemForm(BaseForm):
    name = StringField('Title',
                       validators=[
                            DataRequired(),
                            Length(min=6, max=100,
                                   message="Title must have between " +
                                           "%(min)d and %(max)d characters")
                            ])
    description = TextAreaField('Description',
                                validators=[
                                  DataRequired(),
                                  Length(max=1000,
                                         message="Description must have 1000" +
                                                 " characters max"
                                         )
                                 ])
    categories = OpenSelectMultipleField('Categories')
    photo = FileField('Item photo', validators=[
        FileRequired(),
        FileAllowed(allowed_uploads, 'Only can be an image')
    ])


@app.route('/newitem', methods=['GET', 'POST'])
@login_required
def item_new():
    success = False
    # WTF Form to handle the submitted data
    form = AddItemForm(request.form)
    form.categories.choices = [(str(g.id)+'|'+g.name, g.name) for g
                               in db_session.query(Category).order_by('name')]
    if request.method == 'POST':
        categories_selected = slugify_category_list(form.data['categories'])
        form.categories.choices += [(x[0], x[2]) for x in
                                    categories_selected
                                    if (x[0], x[2]) not in
                                    form.categories.choices]
        if form.validate():
            if len(categories_selected) > 0:
                # Save the new item and the categories selected
                item = Item()
                form.populate_obj(item)
                categories_list = []
                item.categories = categories_list
                for cat_key, cat_id, cat_slug in categories_selected:
                    if cat_id == 0:
                        # New category, create it
                        item_category = Category(name=cat_slug)
                    else:
                        # Find the category by the id
                        item_category = db_session \
                                        .query(Category) \
                                        .filter_by(id=cat_id).first()
                        if item_category is None:
                            # If it wasn't in the database, create it
                            item_category = Category(name=cat_slug)
                    categories_list.append(item_category)
                item.categories = categories_list
                item.author = current_user
                db_session.add(item)
                db_session.commit()
                success = True
                flash("Item was created successfully")
                # Clear the form
                form = AddItemForm(formdata=None)
                form.categories.choices = [(g.name, g.name) for g
                                           in db_session.query(Category)
                                                        .order_by('name')]
            else:
                flash("The item must have at least one category")
    flash_errors(form)
    return render_template('item_form.html', form=form, is_success=success)
