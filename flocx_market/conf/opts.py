import flocx_market.conf

_opts = [
    ('DEFAULT', flocx_market.conf.netconf.opts),
    ('api', flocx_market.conf.api.opts),
    ('flask', flocx_market.conf.flask.opts),
]


def list_opts():
    return _opts
