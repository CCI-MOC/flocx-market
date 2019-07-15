import pytest

from flocx_market.common.service import prepare_service
from flocx_market.conf import CONF
from flocx_market.api.app import create_app
from flocx_market.db.orm import orm
from flocx_market.db.sqlalchemy import api as db_api
from flocx_market.db.sqlalchemy import models as db_models


class test_app_config:
    TESTING = True


@pytest.fixture(scope='session')
def app():
    CONF.clear()
    CONF.set_override("auth_enable", False,
                      group='api')

    prepare_service()
    CONF.set_override('connection', 'sqlite:///:memory:',
                      group='database')
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
    db_api.setup_db()
    yield db_api
    db_api.drop_db()


@pytest.fixture()
def session(db):
    session = db.get_session()
    yield session
    session.close()
    engine = db_api.get_facade().get_engine()
    for table in db_models.Base.metadata.sorted_tables:
        engine.execute(table.delete())
