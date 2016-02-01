from .. import *
import flask_sqlalchemy as sqlalchemy

# Index-related WTForms definitions & views


class SearchForm(BaseForm):
    query = StringField('Search')
    filterbycat = BooleanField('Apply filter', default=False)
    categories = SelectMultipleField('Categories', coerce=int)
    page = IntegerField('Page', default=1)


@app.route('/')
@app.route('/index')
def index():
    # Index view
    # - Displays the index view with a grid with the latest items and filters
    # - that allows to search items by name and description and by categories
    # WTF Form to handle the submitted data
    form = SearchForm(request.args)
    page = form.page.data
    # Fill the category selectbox from the database
    form.categories.choices = [(g.id, g.name) for g in
                               db_session.query(Category).order_by('name')]
    if not form.validate():
        # Reset filters if something went wrong
        page = 1
        form.page.data = page
        form.filterbycat.data = False
        form.categories.data = []
    # Select all the items
    items_query = db_session.query(Item)
    if form.query.data is not None:
        # Filter by form.query value in name and description columns
        items_query = items_query  \
                     .filter(Item.name.ilike('%'+form.query.data+'%') |
                             Item.description.ilike('%'+form.query.data+'%'))
    if form.filterbycat.data is True and len(form.categories.data) > 0:
        # Filter by form.categories values
        # only if the checkbox is selected and there are selected categories in the selectbox
        items_query = items_query  \
                     .filter(Item.categories
                             .any(Category.id.in_(form.categories.data)))
    # Pagination function for the results
    # http://flask-sqlalchemy.pocoo.org/2.1/api/#utilities
    pagination = sqlalchemy \
        .Pagination(items_query, form.page.data,
                    app.config['RESULTS_PER_PAGE'], items_query.count(), None)
    # order and select the results based on the pagination results
    items = items_query \
        .order_by(Item.created_date.desc()) \
        .limit(app.config['RESULTS_PER_PAGE']) \
        .offset((page - 1) * app.config['RESULTS_PER_PAGE']).all()
    return render_template('index.html', form=form,
                           pagination=pagination, items=items, is_index=True)
