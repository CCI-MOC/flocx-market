import flocx_market.conf

_opts = [
    ('DEFAULT', flocx_market.conf.netconf.opts),
    ('api', flocx_market.conf.api.opts),
    ('dummy_node', flocx_market.conf.dummy_node.opts),
    ('flask', flocx_market.conf.flask.opts),
    ('ironic', flocx_market.conf.ironic.list_opts()),
    ('manager', flocx_market.conf.manager.opts),
]


def list_opts():
    return _opts
