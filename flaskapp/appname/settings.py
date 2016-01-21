import tempfile
import os

db_file = tempfile.NamedTemporaryFile()
basedir = os.path.abspath(os.path.dirname(__name__))


class Config(object):
    SECRET_KEY = 'squall-secret-key'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'database.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    STAGING_AREA = os.path.join(basedir, 'assembly')
    CACHE_TYPE = 'simple'
    WTF_CSRF_ENABLED = True


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'database.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    STAGING_AREA = os.path.join(basedir, 'assembly')
    CACHE_TYPE = 'null'
    ASSETS_DEBUG = True
    WTF_CSRF_ENABLED = True


class TestConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, db_file.name)
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    STAGING_AREA = os.path.join(basedir, 'assembly')
    SQLALCHEMY_ECHO = True
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False
