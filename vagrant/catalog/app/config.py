class Config(object):
    HOST = '0.0.0.0'
    PORT = 80
    DEBUG = False
    DEVELOPMENT = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = "postgresql://vagrant:vagrant@localhost/catalog"


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    # PORT = 80
    # HOST = '104.236.18.101'


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    PORT = 5000
