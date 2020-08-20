import os

import pytest

from app import create_app

os.environ["FLASK_CONFIG"] = 'testing'


@pytest.yield_fixture(scope='session')
def app():
    app = create_app()

    with app.app_context():
        yield app


@pytest.fixture
def app_context(app):
    with app.app_context() as ctx:
        yield ctx


@pytest.fixture
def test_client(app, app_context):
    return app.test_client()
