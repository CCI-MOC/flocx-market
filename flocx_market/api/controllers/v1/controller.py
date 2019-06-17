
from pecan import rest
from wsme import types as wtypes

from flocx_market.api import expose as wsexpose


class V1Controller(rest.RestController):


    @wsexpose.expose(wtypes.text)
    def get(self):
        return 'flocx_market v1controller'
