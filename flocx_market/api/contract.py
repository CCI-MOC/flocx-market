from flask_restful import Resource
from flask import request
from flocx_market.objects import contract


class Contract(Resource):

    @classmethod
    def get(cls, contract_id=None):
        if contract_id is None:
            return [x.to_dict() for x in contract.Contract.get_all()]
        c = contract.Contract.get(contract_id)
        if c is None:
            return {'message': 'Contract not found'}, 404
        else:
            return c.to_dict()

    @classmethod
    def post(cls):
        data = request.get_json(force=True)
        return contract.Contract.create(data).to_dict(), 201

    @classmethod
    def delete(cls, contract_id):
        c = contract.Contract.get(contract_id)
        if c is None:
            return {'message': 'Contract not found.'}, 404
        c.destroy()
        return {'message': 'Contract deleted.'}

    @classmethod
    def put(cls, contract_id):
        data = request.get_json(force=True)
        c = contract.Contract.get(contract_id)
        if c is None:
            return {'message': 'Contract not found.'}, 404
        # we only allow status field to be modified
        if 'status' in data:
            c.status = data['status']
            return c.save().to_dict()
        return c.to_dict()
