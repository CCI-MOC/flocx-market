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

from oslo_concurrency import processutils
from oslo_service import service
from oslo_service import wsgi
from flask_migrate import Migrate
from flocx_market.api import app
from flocx_market.db.orm import orm
import flocx_market.conf


CONF = flocx_market.conf.CONF


class WSGIService(service.ServiceBase):

    def __init__(self, name):
        self.name = name
        self.app = app.create_app(app_name='flocx-market')
        Migrate(self.app, orm)
        orm.init_app(self.app)

        self.workers = (
            CONF.api.api_workers or processutils.get_worker_count()
        )

        self.server = wsgi.Server(
            CONF, name, self.app,
            host=CONF.api.host_ip,
            port=CONF.api.port,
            use_ssl=CONF.api.enable_ssl_api
        )

    def start(self):
        self.server.start()

    def stop(self):
        self.server.stop()

    def wait(self):
        self.server.wait()

    def reset(self):
        self.server.reset()
