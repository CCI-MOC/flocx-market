from flask_restful import Resource
from flask import request, g
from flocx_market.objects import bid
from flocx_market.common import exception
import json


class Bid(Resource):

    @classmethod
    def get(cls, marketplace_bid_id=None):

        if marketplace_bid_id is None:
            return [x.to_dict() for x in bid.Bid.get_all(g.context)]

        try:
            return bid.Bid.get(marketplace_bid_id, g.context).to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def post(cls):

        try:
            data = request.get_json(force=True)
            return bid.Bid.create(data, g.context).to_dict(), 201
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def delete(cls, marketplace_bid_id):

        try:
            b = bid.Bid.get(marketplace_bid_id, g.context)
            b.destroy(g.context)
            return {'message': 'Bid deleted.'}
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def put(cls, marketplace_bid_id):

        data = request.get_json(force=True)

        try:
            b = bid.Bid.get(marketplace_bid_id, g.context)
            # we only allow status field to be modified
            if 'status' in data:
                b.status = data['status']
                return b.save(g.context).to_dict()
            return b.to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code
