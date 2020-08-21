import os
from pathlib import Path


class BaseConfig:
    DEBUG = False
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(PROJECT_ROOT, "db.sqlite3"))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    IMAGES_PATH = 'static/images'
    ROOT_DIR = Path(__file__).parent.joinpath('app')


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class TestingConfig(BaseConfig):
    ENV = 'testing'
    TESTING = True

    # Use memory for DB files
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
