from flask_restful import Resource
from flask import request, g
import json

from flocx_market.objects import offer
from flocx_market.common import exception
from flocx_market.common import policy


class Offer(Resource):

    @classmethod
    def get(cls, offer_id=None):
        cdict = g.context.to_policy_values()

        if offer_id is None:
            policy.authorize('flocx_market:offer:get_all', cdict, cdict)
            return [x.to_dict() for x in offer.Offer.get_all(g.context)]
        try:
            policy.authorize('flocx_market:offer:get', cdict, cdict)
            return offer.Offer.get(offer_id, g.context).to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def post(cls):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:offer:create', cdict, cdict)

        try:
            data = request.get_json(force=True)
            return offer.Offer.create(data, g.context).to_dict(), 201
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def delete(cls, offer_id):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:offer:delete', cdict, cdict)

        try:
            o = offer.Offer.get(offer_id, g.context)
            o.destroy(g.context)
            return {'message': 'Offer deleted.'}
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def put(cls, offer_id):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:offer:update', cdict, cdict)

        data = request.get_json(force=True)
        try:
            o = offer.Offer.get(offer_id, g.context)
            # we only allow status field to be modified
            if 'status' in data:
                o.status = data['status']
                return o.save(g.context).to_dict()
            return o.to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code
