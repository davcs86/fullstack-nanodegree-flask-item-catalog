from .. import *
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
        page = 1
    form.categories.choices = [(g.id, g.name) for g in
                               db_session.query(Category).order_by('name')]
    if form.filterbycat.data is False:
        form.categories.data = []
    items_query = db_session.query(Item).filter(Item.id > 0)
    pagination = sqlalchemy \
        .Pagination(items_query, form.page.data, 1,
                    items_query.count(), None)
    items = items_query.limit(1).offset((page - 1) * 1).all()
    # if filter_query is not False:
    #     items = db_session.query(Item) \
    #         .filter((Item.name.ilike(filter_query)) |
    #                 (Item.description.ilike(filter_query))) \
    #         .all()[(page-1)*10::10]
    return render_template('index.html', form=form,
                           pagination=pagination, items=items)
