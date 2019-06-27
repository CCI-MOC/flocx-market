from flask_restful import Resource, reqparse
from flocx_market.db.sqlalchemy.offer_api import OfferApi
from flask import jsonify


class Offer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('provider_id',
                        help="provider_id needed"
                        )
    parser.add_argument('creator_id',
                        help="creator_id needed"
                        )
    parser.add_argument('marketplace_date_created',
                        help="marketplace_date_created needed"
                        )
    parser.add_argument('status',
                        required=True,
                        help="status needed"
                        )
    parser.add_argument('server_id',
                        help="server_id needed"
                        )
    parser.add_argument('start_time',
                        help="start_time needed"
                        )
    parser.add_argument('end_time',
                        help="end_time needed"
                        )
    parser.add_argument('server_config',
                        help="server_config needed"
                        )
    parser.add_argument('cost',
                        help="cost needed"
                        )

    @classmethod
    def get(cls, marketplace_offer_id):
        offer = OfferApi.find_by_id(marketplace_offer_id)
        if offer:
            return offer.as_dict()
        return {'message': 'Offer not found'}, 404

    @classmethod
    def post(cls):
        data = Offer.parser.parse_args()
        offer = OfferApi(**data)
        try:
            offer.save_to_db()
        except:
            return {"message": "An error occurred inserting the offer."}, 500
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
        data = Offer.parser.parse_args()
        offer = OfferApi.find_by_id(marketplace_offer_id)
        offer.status = data['status']
        offer.save_to_db()
        return offer.as_dict()


class OfferList(Resource):
    @classmethod
    def get(cls):
        return {"offers": [x.as_dict() for x in OfferApi.query.all()]}
