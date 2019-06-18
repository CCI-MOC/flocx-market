from pecan import rest
from pecan import expose
from wsme import types as wtypes
from flocx_market.api.controllers.v1 import controller as v1_controller
from flocx_market.api import expose as ep


class CatalogController(rest.RestController):
    @ep.expose(wtypes.text)
    def get(self):
        return "Welcome to the catalog!"


class RootController(rest.RestController):
    # All supported API versions
    _versions = ['v1']

    # The default API version
    _default_version = 'v1'
    v1 = v1_controller.V1Controller()
    # @expose()
    # @unlocked
    # def index(self):
    #     return "public page"

    @ep.expose(wtypes.text)
    def get(self):
        return "flocx_market"
    catalog = CatalogController()
