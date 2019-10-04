from flask_restful import Resource
from flask import request, g
import json

from flocx_market.objects import offer_contract_relationship as ocr
from flocx_market.common import exception
from flocx_market.common import policy


class OfferContractRelationship(Resource):

    @classmethod
    def get(cls, offer_contract_relationship_id=None):
        cdict = g.context.to_policy_values()

        try:
            if offer_contract_relationship_id:
                policy.authorize(
                    'flocx_market:offer_contract_relationship:get',
                    cdict, cdict)
                ocr_with_id = ocr.OfferContractRelationship \
                    .get(g.context, offer_contract_relationship_id)
                return ocr_with_id.to_dict()

            policy.authorize(
                'flocx_market:offer_contract_relationship:get_all',
                cdict, cdict)
            offer_id = request.args.get('offer_id')
            contract_id = request.args.get('contract_id')
            status = request.args.get('status')

            possible_filters = {
                'offer_id': offer_id,
                'contract_id': contract_id,
                'status': status
            }
            filters = {}
            for key, value in possible_filters.items():
                if value is not None:
                    filters[key] = value

            ocrs = ocr.OfferContractRelationship.get_all(g.context, filters)
            if ocrs is None:
                return {'message': 'OfferContractRelationship not found'}, 404

            if type(ocrs) == list:
                return [a.to_dict() for a in ocrs]
            else:
                return ocrs.to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def delete(cls, offer_contract_relationship_id):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:offer_contract_relationship:delete',
                         cdict, cdict)

        try:
            o = ocr.OfferContractRelationship.get(
                                            g.context,
                                            offer_contract_relationship_id)
            o.destroy(g.context)
            return {'message': 'OfferContractRelationship deleted.'}

        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code

    @classmethod
    def put(cls, offer_contract_relationship_id):
        cdict = g.context.to_policy_values()
        policy.authorize('flocx_market:offer_contract_relationship:update',
                         cdict, cdict)

        data = request.get_json(force=True)
        try:
            o = ocr.OfferContractRelationship.get(
                                            g.context,
                                            offer_contract_relationship_id)
            if o is None:
                return {'message': 'OfferContractRelationship not found.'}, 404
            # we only allow status field to be modified
            if 'status' in data:
                o.status = data['status']
                return o.save(g.context).to_dict()
            return o.to_dict()
        except exception.MarketplaceException as e:
            return json.dumps(e.message), e.code
