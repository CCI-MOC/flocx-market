from flask_restful import Resource
from flask import request
from flocx_market.objects import bid


class Bid(Resource):

    @classmethod
    def get(cls, marketplace_bid_id=None):
        if marketplace_bid_id is None:
            return [x.to_dict() for x in bid.Bid.get_all()]
        b = bid.Bid.get(marketplace_bid_id)
        if b is None:
            return {'message': 'Bid not found'}, 404
        else:
            return b.to_dict()

    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        return bid.Bid.create(data).to_dict(), 201

    @classmethod
    def delete(cls, marketplace_bid_id):
        b = bid.Bid.get(marketplace_bid_id)
        if b is None:
            return {'message': 'Bid not found.'}, 404
        b.destroy()
        return {'message': 'Bid deleted.'}

    @classmethod
    def put(cls, marketplace_bid_id):
        data = request.get_json(force=True)
        b = bid.Bid.get(marketplace_bid_id)
        if b is None:
            return {'message': 'Bid not found.'}, 404
        # we only allow status field to be modified
        if 'status' in data:
            b.status = data['status']
            return b.save().to_dict()
        return b.to_dict()
