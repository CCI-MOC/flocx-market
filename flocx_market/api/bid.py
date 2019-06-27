from flask_restful import Resource, reqparse
from flocx_market.db.sqlalchemy.bid_api import BidApid
from flask import jsonify


class Bid(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('creator_bid_id',

                        help="creator_bid_id needed"
                        )
    parser.add_argument('creator_id',
                        help="creator_id needed"
                        )
    parser.add_argument('server_quantity',
                        help="server_quantity needed"
                        )
    parser.add_argument('start_time',
                        help="start_time needed"
                        )
    parser.add_argument('end_time',
                        help="end_time needed"
                        )
    parser.add_argument('duration',
                        help="duration needed"
                        )
    parser.add_argument('status',
                        required=True,
                        help="status needed"
                        )
    parser.add_argument('server_config_query',
                        help="server_config_query needed"
                        )
    parser.add_argument('cost',
                        help="cost needed"
                        )

    @classmethod
    def get(cls, marketplace_bid_id):
        bid = BidApid.find_by_id(marketplace_bid_id)
        if bid:
            return bid.as_dict()
        return {'message': 'Bid not found'}, 404

    @classmethod
    def post(cls):
        data = Bid.parser.parse_args()
        bid = BidApid(**data)
        try:
            bid.save_to_db()
        except:
            return {"message": "An error occurred inserting the bid."}, 500
        return bid.as_dict(), 201

    @classmethod
    def delete(cls, marketplace_bid_id):
        bid = BidApid.find_by_id(marketplace_bid_id)
        if bid:
            bid.delete_from_db()
            return {'message': 'Bid deleted.'}
        return {'message': 'Bid not found.'}, 404

    @classmethod
    def put(cls, marketplace_bid_id):
        data = Bid.parser.parse_args()
        bid = BidApid.find_by_id(marketplace_bid_id)
        if bid is None:
            bid = BidApid(**data)
        else:
            bid.status = data['status']
        bid.save_to_db()
        return bid.as_dict()


class BidList(Resource):
    @classmethod
    def get(cls):
        return {"bids": [x.as_dict() for x in BidApid.query.all()]}
