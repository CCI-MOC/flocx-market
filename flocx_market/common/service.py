
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

from oslo_db import options as db_options
from oslo_log import log
from oslo_service import service

import flocx_market.conf
from flocx_market import version

CONF = flocx_market.conf.CONF


def prepare_service(argv=None, default_config_files=None):
    argv = [] if argv is None else argv
    log.register_options(CONF)
    CONF(argv[1:],
         project='flocx-market',
         version=version.version_info.release_string(),
         default_config_files=default_config_files)
    db_options.set_defaults(CONF)
    log.setup(CONF, 'flocx-market')


def process_launcher():
    return service.ProcessLauncher(CONF, restart_method='mutate')

