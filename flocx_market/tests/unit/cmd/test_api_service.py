import flocx_market.conf
from unittest import mock
import flocx_market.cmd.api as main

CONF = flocx_market.conf.CONF


@mock.patch('flocx_market.cmd.api.flocx_market_service.prepare_service')
@mock.patch('flocx_market.cmd.api.service.ProcessLauncher.launch_service')
@mock.patch('flocx_market.cmd.api.service.ProcessLauncher.wait')
def test_keystone_app(wait, launch, prepare):
    CONF.clear()
    CONF.set_override("auth_enable", True,
                      group='api')

    main.main()

    launch.assert_called_once()
    wait.assert_called_once()
