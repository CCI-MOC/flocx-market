from flask_restful import Resource, reqparse
from flocx_market.models.offer import OfferModel
from flask import jsonify


class Offer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('marketplace_offer_id',
                        required=True,
                        help="marketplace_offer_id needed"
                       )
    parser.add_argument('provider_id',
                        required=True,
                        help="provider_id needed"
                        )
    parser.add_argument('creator_id',
                        required=True,
                        help="creator_id needed"
                        )
    parser.add_argument('marketplace_date_created',
                        required=True,
                        help="marketplace_date_created needed"
                        )
    parser.add_argument('status',
                        required=True,
                        help="status needed"
                        )
    parser.add_argument('server_id',
                        required=True,
                        help="server_id needed"
                        )
    parser.add_argument('start_time',
                        required=True,
                        help="start_time needed"
                        )
    parser.add_argument('end_time',
                        required=True,
                        help="end_time needed"
                        )
    parser.add_argument('server_config',
                        required=True,
                        help="server_config needed"
                        )
    parser.add_argument('cost',
                        required=True,
                        help="cost needed"
                        )

    @classmethod
    def get(cls, marketplace_offer_id):
        offer = OfferModel.find_by_id(marketplace_offer_id)
        if offer:
            return offer.as_dict()
        return {'message': 'Offer not found'}, 404

    @classmethod
    def post(cls):
        data = Offer.parser.parse_args()
        if OfferModel.find_by_id(data['marketplace_offer_id']):
            return {'message': "An offer with marketplace_offer_id '{}' already exists.".format(data['marketplace_offer_id'])}, 400
        offer = OfferModel(**data)
        try:
            offer.save_to_db()
        except:
            return {"message": "An error occurred inserting the offer."}, 500
        return offer.as_dict(), 201

    @classmethod
    def delete(cls, marketplace_offer_id):
        offer = OfferModel.find_by_id(marketplace_offer_id)
        if offer:
            offer.delete_from_db()
            return {'message': 'Offer deleted.'}
        return {'message': 'Offer not found.'}, 404

    @classmethod
    def put(cls, marketplace_offer_id):
        data = Offer.parser.parse_args()
        offer = OfferModel.find_by_id(data['marketplace_offer_id'])
        if offer is None:
            offer = OfferModel(**data)
        else:
            offer.provider_id = data['provider_id']
            offer.creator_id = data['creator_id']
            offer.marketplace_date_created = data['marketplace_date_created']
            offer.status = data['status']
            offer.server_id = data['server_id']
            offer.start_time = data['start_time']
            offer.end_time = data['end_time']
            offer.server_config = data['server_config']
            offer.cost = data['cost']
        offer.save_to_db()
        return offer.as_dict()


class OfferList(Resource):
    @classmethod
    def get(cls):
        return {"offers": [x.as_dict() for x in OfferModel.query.all()]}
