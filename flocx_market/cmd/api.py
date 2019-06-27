from wsgiref import simple_server
from flocx_market.api import app
from flocx_market.common import config as flocx_market_config
import sys
import flocx_market.conf

CONF = flocx_market.conf.CONF

def main():
    flocx_market_config.prepare_service(sys.argv)

    # Build and start the WSGI app
    launcher = flocx_market_config.ProcessLauncher(CONF, restart_method='mutate')
    server = wsgi_service.WSGIService('esi_leap_api')
    launcher.launch_service(server, workers=server.workers)
    launcher.wait()


if __name__ == '__main__':
    main()
