from flask_restful import Resource
from flask import request, g
from flocx_market.objects import contract


class Contract(Resource):

    @classmethod
    def get(cls, contract_id=None):

        if contract_id is None:
            return [x.to_dict() for x in contract.Contract.get_all(g.context)]
        c = contract.Contract.get(contract_id, g.context)
        if c is None:
            return {'message': 'Contract not found'}, 404
        else:
            return c.to_dict()

    @classmethod
    def delete(cls, contract_id):

        c = contract.Contract.get(contract_id, g.context)

        if c is None:
            return {'message': 'Contract not found.'}, 404
        c.destroy(g.context)
        return {'message': 'Contract deleted.'}

    @classmethod
    def put(cls, contract_id):

        data = request.get_json(force=True)
        c = contract.Contract.get(contract_id, g.context)

        if c is None:
            return {'message': 'Contract not found.'}, 404
        # we only allow status field to be modified
        if 'status' in data:
            c.status = data['status']
            return c.save(g.context).to_dict()
        return c.to_dict()
