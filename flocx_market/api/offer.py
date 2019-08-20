from flask_restful import Resource
from flask import request, g
from flocx_market.objects import offer
from flocx_market.common import exception
import json


class Offer(Resource):

    @classmethod
    def get(cls, marketplace_offer_id=None):

        if marketplace_offer_id is None:
            return [x.to_dict() for x in offer.Offer.get_all(g.context)]

        try:
            return offer.Offer.get(marketplace_offer_id, g.context).to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def post(cls):

        try:
            data = request.get_json(force=True)
            return offer.Offer.create(data, g.context).to_dict(), 201
        except (exception.MarketplaceException, exception.InvalidInput) as e:
            return json.dumps(e.message), e.code

    @classmethod
    def delete(cls, marketplace_offer_id):
        try:
            o = offer.Offer.get(marketplace_offer_id, g.context)
            o.destroy(g.context)
            return {'message': 'Offer deleted.'}
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def put(cls, marketplace_offer_id):

        data = request.get_json(force=True)

        try:
            o = offer.Offer.get(marketplace_offer_id, g.context)
            # we only allow status field to be modified
            if 'status' in data:
                o.status = data['status']
                return o.save(g.context).to_dict()
            return o.to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code
