from flask_restful import Resource, reqparse
from flocx_market.db.sqlalchemy.contract_api import ContractApi
from flocx_market.db.sqlalchemy.offer_api import OfferApi
from flask import jsonify
import json


class Contract(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('time_created',
                        help="time_created needed"
                        )
    parser.add_argument('bid_id',
                        help="bid_id needed"
                        )
    parser.add_argument('status',
                        required=True,
                        help="status needed"
                        )
    parser.add_argument('start_time',
                        help="start_time needed"
                        )
    parser.add_argument('end_time',
                        help="end_time needed"
                        )
    parser.add_argument('cost',
                        help="cost needed"
                        )
    parser.add_argument('offers',
                        help="offers needed"
                        )

    @classmethod
    def get(cls, contract_id):
        contract = ContractApi.find_by_id(contract_id)
        if contract:
            return contract.as_dict()
        return {'message': 'Bid not found'}, 404

    @classmethod
    def post(cls):
        data = Contract.parser.parse_args()
        contract = ContractApi(**data)
        try:
            contract.save_to_db()
        except:
            return {"message": "An error occurred inserting the bid."}, 500

        offers = json.loads(data['offers'])
        # need to add foreign key constraint checking here
        for offer in offers:
            selected_offer = OfferApi.find_by_id(offers[offer])
            selected_offer.contract_id = contract.contract_id
            selected_offer.save_to_db()
        return contract.as_dict(), 201

    @classmethod
    def delete(cls, contract_id):
        contract = ContractApi.find_by_id(contract_id)
        if contract:
            contract.delete_from_db()
            return {'message': 'Bid deleted.'}
        return {'message': 'Bid not found.'}, 404

    @classmethod
    def put(cls, contract_id):
        data = Contract.parser.parse_args()
        contract = ContractApi.find_by_id(contract_id)
        contract.status = data['status']
        contract.save_to_db()
        return contract.as_dict()


class ContractList(Resource):
    @classmethod
    def get(cls):
        return {"bids": [x.as_dict() for x in ContractApi.query.all()]}
