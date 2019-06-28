import flocx_market.conf as conf
import socket

CONF = conf.CONF


def test_api_defaults():

    assert(CONF.api.host_ip == "0.0.0.0")
    assert(CONF.api.port == 8081)
    assert(CONF.api.max_limit == 1000)
    assert(CONF.api.public_endpoint is None)
    assert(CONF.api.api_workers is None)
    assert(CONF.api.enable_ssl_api is False)


def test_flask_defaults():

    assert(CONF.flask.SQLALCHEMY_TRACK_MODIFICATIONS is False)
    assert(CONF.flask.PROPAGATE_EXCEPTIONS is False)


def test_netconf_defaults():

    assert(CONF.host == socket.gethostname())
