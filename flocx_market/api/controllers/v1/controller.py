
from pecan import rest
from wsme import types as wtypes
from flocx_market.api.controllers.v1 import offers as v1_offers
from flocx_market.api import expose as wsexpose


class V1Controller(rest.RestController):
    offers = v1_offers.OffersController()
    @wsexpose.expose(wtypes.text)
    def get(self):
        return 'flocx_market v1controller'

