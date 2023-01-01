import secrets
import os


class Config(object):
    DEBUG = False
    TESTING = False
    FLASK_APP = "app.py"
    SECRET_KEY = secrets.token_hex()
    UPLOADS = os.path.join(os.getcwd(), "app", "static/images/profile_pics")
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://test:password@0.0.0.0/blog"


class DevConfig(Config):
    # ENV = "development"
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
    SESSION_COOKIE_SECURE = False


class ProdConfig(Config):
    # ENV = "production"
    FLASK_ENV = "production"
    DEBUG = False
    SESSION_COOKIE_SECURE = True
