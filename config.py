import os
from pathlib import Path


class BaseConfig:
    DEBUG = False
    PROJECT_ROOT = Path(__file__).parent
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", f'sqlite:///{PROJECT_ROOT.joinpath("db.sqlite3")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    IMAGES_PATH = 'static/images'
    ROOT_DIR = PROJECT_ROOT.joinpath('app')


class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class TestingConfig(BaseConfig):
    ENV = 'testing'
    TESTING = True

    # Use memory for DB files
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
