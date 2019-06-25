from oslo_config import cfg

from flocx_market.conf import api
from flocx_market.conf import netconf
from flocx_market.conf import flask


CONF = cfg.CONF


CONF.register_group(cfg.OptGroup(name='database'))
api.register_opts(CONF)
netconf.register_opts(CONF)
flask.register_opts(CONF)
