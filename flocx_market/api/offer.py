from flask_restful import Resource
from flask import request
from flocx_market.db.sqlalchemy import api as dbapi


class Offer(Resource):

    @classmethod
    def get(cls, marketplace_offer_id=None):
        if marketplace_offer_id is None:
            return OfferList.get()['offers']

        offer = dbapi.offer_get(marketplace_offer_id)
        if offer:
            return offer.to_dict()
        return {'message': 'Offer not found'}, 404

    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        offer = dbapi.offer_create(**data)
        return offer.to_dict(), 201

    @classmethod
    def delete(cls, marketplace_offer_id):
        offer = dbapi.offer_get(marketplace_offer_id)
        if offer:
            dbapi.offer_destroy(marketplace_offer_id)
            return {'message': 'Offer deleted.'}
        return {'message': 'Offer not found.'}, 404

    @classmethod
    def put(cls, marketplace_offer_id):
        data = request.get_json(force=True)
        offer = dbapi.offer_get(marketplace_offer_id)
        if offer is None:
            return {'message': 'Offer not found'}, 404

        offer.status = data['status']
        dbapi.offer_update(marketplace_offer_id, offer.to_dict())
        return offer.to_dict()


class OfferList(Resource):
    @classmethod
    def get(cls):
        return {"offers": [x.to_dict() for x in dbapi.offer_get_all()]}
