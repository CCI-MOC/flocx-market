from flask_restful import Resource
from flask import request
from flocx_market.db.sqlalchemy.offer_api import OfferApi
from flask import jsonify


class Offer(Resource):

    @classmethod
    def get(cls, marketplace_offer_id):
        offer = OfferApi.find_by_id(marketplace_offer_id)
        if offer:
            return offer.as_dict()
        return {'message': 'Offer not found'}, 404

    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        data_for_offer = [x for x in data.values()]
        offer = OfferApi(*data_for_offer)
        offer.save_to_db()
        return offer.as_dict(), 201

    @classmethod
    def delete(cls, marketplace_offer_id):
        offer = OfferApi.find_by_id(marketplace_offer_id)
        if offer:
            offer.delete_from_db()
            return {'message': 'Offer deleted.'}
        return {'message': 'Offer not found.'}, 404

    @classmethod
    def put(cls, marketplace_offer_id):
        data = request.get_json(force=True)
        offer = OfferApi.find_by_id(marketplace_offer_id)
        offer.status = data['status']
        offer.save_to_db()
        return offer.as_dict()


class OfferList(Resource):
    @classmethod
    def get(cls):
        return {"offers": [x.as_dict() for x in OfferApi.query.all()]}
