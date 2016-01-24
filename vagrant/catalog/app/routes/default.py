from .. import app, db


@app.route('/')
@app.route('/index')
def index():
    return 'Hola'
