from oslo_config import cfg

from flocx_market.conf import api
from flocx_market.conf import dummy_node
from flocx_market.conf import ironic
from flocx_market.conf import netconf
from flocx_market.conf import flask
from flocx_market.conf import manager


CONF = cfg.CONF


CONF.register_group(cfg.OptGroup(name='database'))
api.register_opts(CONF)
dummy_node.register_opts(CONF)
ironic.register_opts(CONF)
netconf.register_opts(CONF)
flask.register_opts(CONF)
manager.register_opts(CONF)
