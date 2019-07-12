from flask_restful import Resource
from flask import request
from flocx_market.db.sqlalchemy import offer_api


class Offer(Resource):

    @classmethod
    def get(cls, marketplace_offer_id=None):
        if marketplace_offer_id is None:
            return OfferList.get()['offers']

        offer = offer_api.get(marketplace_offer_id)
        if offer:
            return offer.to_dict()
        return {'message': 'Offer not found'}, 404

    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        offer = offer_api.create(**data)
        return offer.to_dict(), 201

    @classmethod
    def delete(cls, marketplace_offer_id):
        offer = offer_api.get(marketplace_offer_id)
        if offer:
            offer_api.destroy(marketplace_offer_id)
            return {'message': 'Offer deleted.'}
        return {'message': 'Offer not found.'}, 404

    @classmethod
    def put(cls, marketplace_offer_id):
        data = request.get_json(force=True)
        offer = offer_api.get(marketplace_offer_id)
        if offer is None:
            return {'message': 'Offer not found'}, 404

        offer.status = data['status']
        offer_api.update(marketplace_offer_id, offer.to_dict())
        return offer.to_dict()


class OfferList(Resource):
    @classmethod
    def get(cls):
        return {"offers": [x.to_dict() for x in offer_api.get_all()]}
