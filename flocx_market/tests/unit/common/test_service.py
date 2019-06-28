import flocx_market.conf as conf
import socket
import flocx_market.common.service as flocx_market_service
import pytest
import unittest.mock as mock

CONF = conf.CONF


@mock.patch('oslo_config.cfg.find_config_files')
def test_service_defaults(find_config_files):

    CONF.clear()
    flocx_market_service.prepare_service()
    assert(CONF.api.host_ip == "0.0.0.0")
    assert(CONF.api.port == 8081)
    assert(CONF.api.max_limit == 1000)
    assert(CONF.api.public_endpoint is None)
    assert(CONF.api.api_workers is None)
    assert(CONF.api.enable_ssl_api is False)
    assert(CONF.flask.SQLALCHEMY_TRACK_MODIFICATIONS is False)
    assert(CONF.flask.PROPAGATE_EXCEPTIONS is False)
    assert(CONF.host == socket.gethostname())


@mock.patch('oslo_config.cfg.find_config_files')
def test_service_cli_valid(find_config_files):

    CONF.clear()
    args = ['dummy', '--api-port', '8085', '--api-host_ip', '0.0.0.1',
            '--api-public_endpoint', '/index', '--api-api_workers', '5', '--api-enable_ssl',
            '--flask-noSQLALCHEMY_TRACK_MODIFICATIONS', '--flask-PROPAGATE_EXCEPTIONS', '--host', 'imhost']

    flocx_market_service.prepare_service(argv=args)
    assert(CONF.api.port == int(args[args.index('--api-port') + 1]))
    assert(CONF.api.host_ip == str(args[args.index('--api-host_ip') + 1]))
    assert(CONF.api.public_endpoint == str(args[args.index('--api-public_endpoint') + 1]))
    assert(CONF.api.api_workers == int(args[args.index('--api-api_workers') + 1]))
    assert(CONF.api.enable_ssl_api)

    assert(CONF.api.max_limit == 1000)

    assert(CONF.flask.SQLALCHEMY_TRACK_MODIFICATIONS is False)
    assert(CONF.flask.PROPAGATE_EXCEPTIONS)

    assert(CONF.host == str(args[args.index('--host') + 1]))


@mock.patch('oslo_config.cfg.find_config_files')
def test_service_cli_invalid_option(find_config_files):
    CONF.clear()
    with pytest.raises(SystemExit) as excinfo:
        flocx_market_service.prepare_service(
            argv=['dummy', '--badarg'])

    assert excinfo.value.code == 2


@mock.patch('oslo_config.cfg.find_config_files')
def test_service_cli_invalid_value(find_config_files):
    CONF.clear()
    with pytest.raises(SystemExit) as excinfo:
        flocx_market_service.prepare_service(
            argv=['dummy', '--api-port', 'notInt'])

    assert excinfo.value.code is None
