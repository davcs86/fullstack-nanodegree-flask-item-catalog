import tempfile


class Config(object):
    HOST = '0.0.0.0'
    PORT = 80
    DEBUG = False
    DEVELOPMENT = False
    WTF_CSRF_ENABLED = False
    CSRF_COOKIE_NAME = '_csrf_token'
    SECRET_KEY = 'UNbPflgB8ZNQPwdY9m5owtstQwGIKIJXXfjuJeFwIYl6Mz3UqNT6VwPKBQW9'
    UPLOAD_FOLDER = tempfile.tempdir
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    SQLALCHEMY_DATABASE_URI = "postgresql://vagrant:vagrant@localhost/catalog"
    RESULTS_PER_PAGE = 10
    ENDPOINT_RESULTS_PER_PAGE = 25
    OAUTH_CREDENTIALS = {
        'google': {
            'id': '',
            'secret': ''
        },
        'facebook': {
            'id': '1695511664028594',
            'secret': '2849bb510817adc71821d7daff76e090'
        },
        'twitter': {
            'id': 'WToKwwI3emnoiMUjDQWoDGp6e',
            'secret': 'PAdJYOth7IztOcSjaeSMIaK1arVZ7BDvOc3dbX4mchec5tdkSN'
        },
        'github': {
            'id': '1be4ae8a83efbb356ad8',
            'secret': 'b8fe0ab54bea0640c9117accf57e34e01c3b1c32'
        }
    }


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    # PORT = 80
    # HOST = '104.236.18.101'


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    PORT = 5000
    RESULTS_PER_PAGE = 1
