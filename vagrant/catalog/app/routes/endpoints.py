from .. import *
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from flask import jsonify

# Endpoint-related definitions


def make_external(url):
    # Resolve the external url
    return urljoin(request.url_root, url)


@app.route('/recent_items.atom')
def recent_feed():
    # Create an atom feed with the latest items
    # the number of items is given by the setting ENDPOINT_RESULTS_PER_PAGE
    # Based on: http://flask.pocoo.org/snippets/10/
    feed = AtomFeed('Recent Items',
                    feed_url=request.url, url=request.url_root,
                    author={'name': 'David Castillo',
                            'email': 'davcs86@gmail.com',
                            'uri': 'http://github.com/davcs86'},
                    generator=('self generated', '', '0.1'))
    # query the items
    items = db_session.query(Item).order_by(Item.created_date.desc()) \
                      .limit(app.config['ENDPOINT_RESULTS_PER_PAGE']).all()
    # add them to the feed
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
    # Create a json file with the latest items
    # the number of items is given by the setting ENDPOINT_RESULTS_PER_PAGE
    items = db_session.query(Item).order_by(Item.created_date.desc()) \
                      .limit(app.config['ENDPOINT_RESULTS_PER_PAGE']).all()
    return jsonify(Items=[i.serialize for i in items])
