from flask_restful import Resource
from flask import request, g
import json

from flocx_market.objects import bid
from flocx_market.common import exception
from flocx_market.common import policy


class Bid(Resource):

    @classmethod
    def get(cls, bid_id=None):
        cdict = g.context.to_policy_values()

        if bid_id is None:
            policy.authorize('flocx_market:bid:get_all', cdict, cdict)
            return [x.to_dict() for x in bid.Bid.get_all(g.context)]
        try:
            policy.authorize('flocx_market:bid:get', cdict, cdict)
            return bid.Bid.get(bid_id, g.context).to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def post(cls):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:bid:create', cdict, cdict)

        try:
            data = request.get_json(force=True)
            return bid.Bid.create(data, g.context).to_dict(), 201
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def delete(cls, bid_id):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:bid:delete', cdict, cdict)

        try:
            b = bid.Bid.get(bid_id, g.context)
            b.destroy(g.context)
            return {'message': 'Bid deleted.'}
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def put(cls, bid_id):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:bid:update', cdict, cdict)

        data = request.get_json(force=True)
        try:
            b = bid.Bid.get(bid_id, g.context)
            # we only allow status field to be modified
            if 'status' in data:
                b.status = data['status']
                return b.save(g.context).to_dict()
            return b.to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code
