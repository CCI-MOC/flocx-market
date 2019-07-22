from oslo_config import cfg

from flocx_market.conf import api
from flocx_market.conf import netconf
from flocx_market.conf import flask
from flocx_market.conf import manager


CONF = cfg.CONF


CONF.register_group(cfg.OptGroup(name='database'))
api.register_opts(CONF)
netconf.register_opts(CONF)
flask.register_opts(CONF)
manager.register_opts(CONF)
