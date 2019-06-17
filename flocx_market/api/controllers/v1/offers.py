import datetime
import pecan
from pecan import request
from pecan import rest
import wsme
from wsme import types as wtypes

from flocx_market.api import expose
from flocx_market.api.controllers import types

class Offer(wtypes.Base):
    id = int
    marketplace_offer_id = wtypes.text
    provider_id = wtypes.text
    creator_id = wtypes.text
    marketplace_date_created = wsme.wsattr(datetime.datetime)
    status = wtypes.text
    server_name = wtypes.text
    start_time = wsme.wsattr(datetime.datetime)
    end_time = wsme.wsattr(datetime.datetime)
    duration = int
    server_config = {wtypes.text: types.jsontype}
    cost = int


class Offers(wtypes.Base):
    offers = [Offer]


class OffersController(rest.RestController):
    @pecan.expose()
    def _lookup(self, offer_id, *remainder):
        return OfferController(offer_id), remainder

    @expose.expose(Offers)
    def get(self):
        db_conn = request.db_conn
        offers = db_conn.list_offers()
        offers_list = []
        for offer in offers:
            o = Offer()
            o.id = offer.id
            o.marketplace_offer_id = offer.marketplace_offer_id
            o.provider_id = offer.provider_id
            o.marketplace_date_created = offer.marketplace_date_created
            o.status = offer.status
            o.server_name = offer.server_name
            o.start_time = offer.start_time
            o.end_time = offer.end_time
            o.duration = offer.duration
            o.server_config = offer.server_config
            o.cost = offer.cost
            offers_list.append(o)
        return Offers(offers=offers_list)

    @expose.expose(None, body=Offer, status_code=201)
    def post(self, offer):
        print (offer)
