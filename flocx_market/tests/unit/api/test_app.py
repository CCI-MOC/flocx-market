import json
import pytest

from oslo_config import cfg

import flocx_market.api.app
import flocx_market.conf

CONF = flocx_market.conf.CONF


@pytest.fixture
def test_app():
    CONF.set_override("auth_enable", False,
                      group='api')
    connection_opt = cfg.StrOpt("connection", None)
    CONF.register_opt(connection_opt, group="database")
    app = flocx_market.api.app.create_app(app_name="test").test_client()
    app.testing = True
    yield app
    CONF.unregister_opt(connection_opt, group="database")


def test_root_status_code(test_app):
    response = test_app.get("/", follow_redirects=True)
    assert response.status_code == 200


def test_root_data(test_app):
    response = test_app.get("/", follow_redirects=True)
    flocx_market_url = CONF.api.host_ip + ":" + str(CONF.api.port)
    version = {
        "versions": {
            "values": [{
                "status":
                "in progress",
                "updated":
                "2019-07-02T00:00:00Z",
                "media-types": [{
                    "base": "application/json",
                    "name": "flocx-market"
                }],
                "links": [{
                    "href": flocx_market_url,
                    "rel": "self"
                }]
            }]
        }
    }
    assert json.loads(response.data) == version
