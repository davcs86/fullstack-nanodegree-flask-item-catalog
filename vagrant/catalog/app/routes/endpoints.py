from .. import *
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from flask import jsonify


def make_external(url):
    return urljoin(request.url_root, url)


@app.route('/recent_items.atom')
def recent_feed():
    feed = AtomFeed('Recent Items',
                    feed_url=request.url, url=request.url_root,
                    author={'name': 'David Castillo',
                            'email': 'davcs86@gmail.com',
                            'uri': 'http://github.com/davcs86'},
                    generator=('self generated', '', '0.1'))
    items = db_session.query(Item).order_by(Item.created_date.desc()) \
                      .limit(app_config.ENDPOINT_RESULTS_PER_PAGE).all()
    for item in items:
        feed.add(item.name, unicode(item.description),
                 content_type='html',
                 author=item.author.nickname,
                 url=make_external(url_for('item_detail', item_id=item.id)),
                 categories=[{'name': g.name} for g in item.categories],
                 updated=item.updated_date,
                 links=[{'href': g.locate(), 'rel': 'enclosure',
                         'type': g.mimetype} for g in item.picture.all()],
                 published=item.created_date)
    return feed.get_response()


@app.route('/recent_items.json')
def recent_json():
    items = db_session.query(Item).order_by(Item.created_date.desc()) \
                      .limit(app_config.ENDPOINT_RESULTS_PER_PAGE).all()
    return jsonify(Items=[i.serialize for i in items])
