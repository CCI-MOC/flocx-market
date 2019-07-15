from flask_restful import Resource
from flocx_market.db.sqlalchemy.bid_api import BidApi
from flask import request


class Bid(Resource):

    @classmethod
    def get(cls, marketplace_bid_id=None):
        if marketplace_bid_id is None:
            return BidList.get()['bids']
        bid = BidApi.find_by_id(marketplace_bid_id)
        if bid:
            return bid.as_dict()
        return {'message': 'Bid not found'}, 404

    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        bid = BidApi(**data)
        bid.save_to_db()
        return bid.as_dict(), 201

    @classmethod
    def delete(cls, marketplace_bid_id):
        bid = BidApi.find_by_id(marketplace_bid_id)
        if bid:
            bid.delete_from_db()
            return {'message': 'Bid deleted.'}
        return {'message': 'Bid not found.'}, 404

    @classmethod
    def put(cls, marketplace_bid_id):
        data = request.get_json(force=True)
        bid = BidApi.find_by_id(marketplace_bid_id)
        if bid is None:
            return {'message': 'Bid not found.'}, 404

        bid.status = data['status']
        bid.save_to_db()
        return bid.as_dict()


class BidList(Resource):
    @classmethod
    def get(cls):
        return {"bids": [x.as_dict() for x in BidApi.query.all()]}
