from oslo_db import options as db_options
from oslo_log import log
from oslo_service import service

import flocx_market.conf
from flocx_market import objects
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
    objects.register_all()


def process_launcher():
    return service.ProcessLauncher(CONF, restart_method='mutate')
