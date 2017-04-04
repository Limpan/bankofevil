import os


class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'very hard to guess string'
    if os.environ.get('SENTRY_DSN', False):
        SENTRY_DSN = os.environ.get('SENTRY_DSN')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
    'postgresql+psycopg2://postgres:secretpassword@postgresql/development'


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'

    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or \
    'postgresql+psycopg2://postgres:secretpassword@postgresql/testing'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    'postgresql+psycopg2://postgres:secretpassword@postgresql/production'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
