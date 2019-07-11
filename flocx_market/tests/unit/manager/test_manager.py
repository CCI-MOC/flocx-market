import flocx_market.conf as conf
import flocx_market.manager.service as manager
import flocx_market.cmd.manager as main

from unittest import mock
CONF = conf.CONF


@mock.patch('flocx_market.cmd.manager.service._check_service_base')
@mock.patch('flocx_market.cmd.manager.manager_service.ManagerService')
@mock.patch('flocx_market.cmd.manager.flocx_market_service.prepare_service')
@mock.patch('flocx_market.cmd.manager.manager_service.ManagerService.start')
@mock.patch('flocx_market.cmd.manager.service.Launcher.wait')
def test_launch_service_manager(wait, startmock, prepare, managermock, base):

    CONF.clear()
    main.main()

    wait.assert_called()
    managermock.assert_called()


@mock.patch('flocx_market.manager.service.threadgroup.ThreadGroup.'
            'add_dynamic_timer')
def test_start_manager(timer):
    m = manager.ManagerService()
    m.tasks.run_periodic_tasks(None)
    m.start()

    timer.assert_called()
