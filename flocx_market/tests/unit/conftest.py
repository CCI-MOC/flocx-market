import pytest

from flocx_market.common.service import prepare_service
from flocx_market.conf import CONF
from flocx_market.api.app import create_app
from flocx_market.db.orm import orm


class test_app_config:
    TESTING = True


@pytest.fixture(scope='session')
def app():
    CONF.clear()
    prepare_service()
    CONF.database.connection = 'sqlite:///:memory:'
    app = create_app('testing')
    app.config.from_object(test_app_config)
    orm.init_app(app)
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.push()


@pytest.fixture(scope='session')
def client(app):
    _client = app.test_client()
    _client.testing = True
    return _client


@pytest.fixture()
def db(app):
    orm.create_all()
    yield orm
    orm.drop_all()


@pytest.fixture()
def session(db):
    session = db.session()
    yield session
    if not session.transaction.is_active:
        session.rollback()
