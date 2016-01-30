from .. import *
import sqlalchemy as is_
import flask_sqlalchemy as sqlalchemy


class SearchForm(BaseForm):
    query = StringField('Search')
    filterbycat = BooleanField('Apply filter', default=False)
    categories = SelectMultipleField('Categories')
    page = IntegerField('Page', default=1)


@app.route('/')
@app.route('/index')
def index():
    form = SearchForm(request.args)
    page = form.page.data
    if not form.validate():
        # Reset filters if something went wrong
        page = 1
        form.page.data = page
        form.filterbycat.data = False
        form.categories.data = []

    form.categories.choices = [(g.id, g.name) for g in
                               db_session.query(Category).order_by('name')]
    items_query = db_session.query(Item, ItemCategory, Category)
    if form.query.data is not None:
        items_query = items_query  \
                     .filter(is_(Item.name.ilike('%'+form.query.data+'%')))  #|
                             # (Item.description.ilike(form.query.data)))
    if form.filterbycat.data is False:
        form.categories.data = []
    elif len(form.categories.data) > 0:
        items_query = items_query  \
                     .filter(Item.categories
                             .any(Category.id.in_(form.categories.data)))

    pagination = sqlalchemy \
        .Pagination(items_query, form.page.data, 1,
                    items_query.count(), None)
    items = items_query \
        .limit(app_config.RESULTS_PER_PAGE) \
        .offset((page - 1) * app_config.RESULTS_PER_PAGE).all()
    return render_template('index.html', form=form,
                           pagination=pagination, items=items)
