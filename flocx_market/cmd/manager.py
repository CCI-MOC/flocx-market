import sys

from oslo_service import service

from flocx_market.common import service as flocx_market_service
import flocx_market.conf
from flocx_market.manager import service as manager_service


CONF = flocx_market.conf.CONF


def main():
    flocx_market_service.prepare_service(sys.argv)

    service.launch(
        CONF,
        manager_service.ManagerService(),
        restart_method='mutate'
    ).wait()


if __name__ == '__main__':
    sys.exit(main())
