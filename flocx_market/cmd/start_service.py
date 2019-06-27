#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import sys

from oslo_service import service

from flocx_market.api import service as wsgi_service
from flocx_market.common import service as flocx_market_service
import flocx_market.conf

CONF = flocx_market.conf.CONF


def main():
    flocx_market_service.prepare_service(sys.argv)
    # Build and start the WSGI app
    launcher = service.ProcessLauncher(CONF, restart_method='mutate')
    server = wsgi_service.WSGIService('flocx_market_api')
    launcher.launch_service(server, workers=server.workers)
    launcher.wait()

if __name__ == '__main__':
    main()