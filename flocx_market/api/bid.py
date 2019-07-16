from flask_restful import Resource
from flask import request
from flocx_market.db.sqlalchemy import api as dbapi


class Bid(Resource):

    @classmethod
    def get(cls, marketplace_bid_id=None):
        if marketplace_bid_id is None:
            return BidList.get()['bids']

        bid = dbapi.bid_get(marketplace_bid_id)
        if bid:
            return bid.to_dict()
        return {'message': 'Bid not found'}, 404

    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        bid = dbapi.bid_create(data)
        return bid.to_dict(), 201

    @classmethod
    def delete(cls, marketplace_bid_id):
        bid = dbapi.bid_get(marketplace_bid_id)
        if bid:
            dbapi.bid_destroy(marketplace_bid_id)
            return {'message': 'Bid deleted.'}
        return {'message': 'Bid not found.'}, 404

    @classmethod
    def put(cls, marketplace_bid_id):
        data = request.get_json(force=True)
        bid = dbapi.bid_get(marketplace_bid_id)
        if bid is None:
            return {'message': 'Bid not found.'}, 404

        bid.status = data['status']
        dbapi.bid_update(marketplace_bid_id, bid.to_dict())
        return bid.to_dict()


class BidList(Resource):
    @classmethod
    def get(cls):
        return {"bids": [x.to_dict() for x in dbapi.bid_get_all()]}
