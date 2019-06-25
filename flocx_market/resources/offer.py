from flask_restful import Resource, reqparse
from flocx_market.models.offer import OfferModel


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
                        type=int,
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

    def get(self, marketplace_offer_id):
        offer = OfferModel.find_by_id(marketplace_offer_id)
        if offer:
            return offer.json()
        return {'message': 'Offer not found'}, 404

# marketplace_offer_id, provider_id, creator_id, marketplace_date_created, status, server_id, start_time, end_time,
    # server_config, cost
    def post(self):
        data = Offer.parser.parse_args()
        if OfferModel.find_by_id(data['marketplace_offer_id']):
            return {'message': "An offer with marketplace_offer_id '{}' already exists.".format(data['marketplace_offer_id'])}, 400
        offer = OfferModel(**data)
        try:
            offer.save_to_db()
        except Exception:
            return {"message": "An error occurred inserting the offer."}, 500
        return offer.json(), 201

    def delete(self, marketplace_offer_id):
        offer = OfferModel.find_by_id(marketplace_offer_id)
        if offer:
            offer.delete_from_db()
            return {'message': 'Offer deleted.'}
        return {'message': 'Offer not found.'}, 404

    def put(self, marketplace_offer_id):
        data = Offer.parse.parse_args()
        offer = OfferModel.find_by_id(marketplace_offer_id)
        if offer:
            offer = OfferModel(marketplace_offer_id, **data)
        offer.save_to_db()
        return offer.json()


class OfferList(Resource):
    def get(self):
        return {"offers": [x.json() for x in OfferModel.query.all()]}
