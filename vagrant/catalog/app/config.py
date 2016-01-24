class Config(object):
    HOST = '0.0.0.0'
    PORT = 80
    DEBUG = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = "postgresql://vagrant:vagrant@localhost/catalog"
    GOOGLE_LOGIN_CLIENT_ID = "<your-id-ending-with>.apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "<your-secret>"
    OAUTH_CREDENTIALS = {
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        },
        'facebook': {
            'id': '1695511664028594',
            'secret': '2849bb510817adc71821d7daff76e090'
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
