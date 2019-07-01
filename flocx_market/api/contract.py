from flask_restful import Resource
from flask import request
from flocx_market.db.sqlalchemy import api as dbapi


def contract_with_offers(contract_obj):
    contract_data = contract_obj.to_dict()
    offer_model_objects = [offer for offer in contract_obj.offers.all()]
    # needed to avoid foreign key constraint issue here
    offer_api_ids = []
    for offer in offer_model_objects:
        for column in offer.__table__.columns:
            if column.name == "marketplace_offer_id":
                offer_api_obj = dbapi.offer_get(getattr(offer,
                                                        column.name))
                offer_api_ids.append(offer_api_obj.marketplace_offer_id)

    if offer_api_ids:
        contract_data["offers"] = [offer_id for offer_id in offer_api_ids]

    return contract_data


class Contract(Resource):

    @classmethod
    def get(cls, contract_id=None):
        if contract_id is None:
            return ContractList.get()['contracts']

        contract = dbapi.contract_get(contract_id)
        if contract:
            return contract_with_offers(contract)
        return {'message': 'Contract not found'}, 404

    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        contract = dbapi.contract_create(data)
        return contract_with_offers(contract), 201

    @classmethod
    def delete(cls, contract_id):
        contract = dbapi.contract_get(contract_id)
        if contract:
            dbapi.contract_destroy(contract_id)
            return {'message': 'Contract deleted.'}
        return {'message': 'Contract not found.'}, 404

    @classmethod
    def put(cls, contract_id):
        data = request.get_json(force=True)
        contract = dbapi.contract_get(contract_id)
        if contract is None:
            return {'message': 'Contract not found.'}, 404

        contract.status = data['status']
        dbapi.contract_update(contract_id, contract_with_offers(contract))
        return contract_with_offers(contract)


class ContractList(Resource):
    @classmethod
    def get(cls):
        return {"contracts": [
            contract_with_offers(c) for c in dbapi.contract_get_all()
        ]}
