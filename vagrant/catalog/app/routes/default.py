from .. import app, session


@app.route('/')
@app.route('/index')
def index():
    return 'Hola'
