from .. import *


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


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
    picture = FileField('Item picture')

    def validate_picture(form, field):
        if field.name in request.files:
            field.data = request.files[field.name]
            if not allowed_file(field.data.filename):
                raise ValidationError('Item picture must be an image')
        else:
            field.data = None


class EditItemForm(BaseForm):
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
    picture = FileField('Item picture')
    # 0 = unmodified; 1 = replaced; 2 = deleted
    picture_status = IntegerField('picture_status')

    def validate_picture(form, field):
        if form.picture_status.data == '1':  # validate only if it was modified
            if field.name in request.files:
                # store the file
                field.data = request.files[field.name]
                if not allowed_file(field.data.filename):
                    raise ValidationError('Item picture must be an image')
        else:
            field.data = None


@app.route('/item/new', methods=['GET', 'POST'])
@login_required
def item_new():
    success = False
    # WTF Form to handle the submitted data
    form = AddItemForm(request.form)
    form.categories.choices = [(str(g.id)+'|'+g.name, g.name) for g
                               in db_session.query(Category).order_by('name')]
    if request.method == 'POST':
        categories_selected = slugify_category_list(form.categories.data)
        form.categories.choices += [(x[0], x[2]) for x in
                                    categories_selected
                                    if (x[0], x[2]) not in
                                    form.categories.choices]
        if form.validate():
            if len(categories_selected) > 0:
                # Save the new item and the categories selected
                item = Item()
                item.name = form.name.data
                item.description = form.description.data
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
                if form.picture.data is not None:
                    item.picture.from_blob(
                        form.picture.data.read())
                db_session.add(item)
                db_session.commit()
                success = True
                flash("Item was created successfully")
                # Clear the form, reset the categories
                form = AddItemForm(formdata=None)
                form.categories \
                    .choices = [(str(g.id)+'|'+g.name, g.name) for g
                                in db_session.query(Category).order_by('name')]
            else:
                flash("The item must have at least one category")
    flash_errors(form)
    return render_template('item_form.html', form=form, is_success=success)


@app.route('/item/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def item_edit(item_id):
    success = False
    # verify if the item exists and if current_user is its author
    item = db_session.query(Item) \
                     .filter(Item.id == item_id and
                             Item.author_id == current_user.id).first()
    if item is None:
        flash("You can only modify your own items")
        return redirect(url_for('index'))
    # WTF Form to handle the submitted data
    form = EditItemForm(request.form, item)
    form.categories.choices = [(str(g.id)+'|'+g.name, g.name) for g
                               in db_session.query(Category).order_by('name')]
    if request.method == 'GET':
        form.picture_status.data = 0
        form.categories.data = [str(g.id)+'|'+g.name for g in item.categories]
    elif request.method == 'POST':
        categories_selected = slugify_category_list(form.categories.data)
        form.categories.choices += [(x[0], x[2]) for x in
                                    categories_selected
                                    if (x[0], x[2]) not in
                                    form.categories.choices]
        if form.validate():
            if len(categories_selected) > 0:
                item.name = form.name.data
                item.description = form.description.data
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
                if form.picture_status.data == '2' \
                   or form.picture_status.data == '1':
                    # delete the current image
                    current_image = item.picture.first()
                    if current_image is not None:
                        item.picture.remove(current_image)
                if form.picture_status.data == '1':
                    if form.picture.data is not None:
                        item.picture.from_blob(
                            form.picture.data.read())
                db_session.merge(item)
                db_session.commit()
                success = True
                flash("Item was modified successfully")
                # reset the form
                form = EditItemForm(request.form, item)
                form.categories \
                    .choices = [(str(g.id)+'|'+g.name, g.name) for g
                                in db_session.query(Category).order_by('name')]
                form.picture_status.data = 0
                form.categories.data = [str(g.id)+'|'+g.name for g
                                        in item.categories]
            else:
                flash("The item must have at least one category")
    flash_errors(form)
    # retrieve the current item image
    item_image_url = False
    current_image = item.picture.first()
    if current_image is not None:
        item_image_url = item.picture.locate()
    return render_template('item_form.html', item_image_url=item_image_url,
                           form=form, is_success=success, is_edit=True,
                           item_id=item.id)


@app.route('/item/detail/<int:item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = db_session.query(Item) \
                     .filter(Item.id == item_id).first()
    if item is None:
        flash('Item does not exist')
        return redirect(url_for('index'))
    return render_template('item_detail.html', item=item)
