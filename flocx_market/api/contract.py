from flask_restful import Resource
from flask import request, g
import json

from flocx_market.objects import contract
from flocx_market.common import exception
from flocx_market.common import policy


class Contract(Resource):

    @classmethod
    def get(cls, contract_id=None):
        cdict = g.context.to_policy_values()

        if contract_id is None:
            policy.authorize('flocx_market:contract:get_all', cdict, cdict)
            return [x.to_dict() for x in contract.Contract.get_all(g.context)]
        try:
            policy.authorize('flocx_market:contract:get', cdict, cdict)
            return contract.Contract.get(contract_id, g.context).to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def post(cls):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:contract:create', cdict, cdict)

        data = request.get_json(force=True)
        try:
            return contract.Contract.create(data, g.context).to_dict(), 201
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def delete(cls, contract_id):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:contract:delete', cdict, cdict)

        try:
            c = contract.Contract.get(contract_id, g.context)
            c.destroy(g.context)
            return {'message': 'Contract deleted.'}
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def put(cls, contract_id):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:contract:update', cdict, cdict)

        data = request.get_json(force=True)
        try:
            c = contract.Contract.get(contract_id, g.context)
            # we only allow status field to be modified
            if 'status' in data:
                c.status = data['status']
                return c.save(g.context).to_dict()
            return c.to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code
