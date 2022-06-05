import os
import pytest

from src import db
from src import init_app


@pytest.fixture()
def app():
    app = init_app(test=True)

    db.init_app(app)  # initialise the database for the app
    with app.app_context():
        # always starting with an empty DB
        db.drop_all()
        db.create_all()
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
