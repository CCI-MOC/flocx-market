import flocx_market.conf as conf
from flocx_market.common import config as flocx_market_config
import sys
CONF = conf.CONF


def test_keystone_default():
    flocx_market_config.prepare_service(sys.argv)

    print (CONF.api.port)
    # print (CONF.keystone_authtoken.username)


test_keystone_default()
