from flask_restful import Resource
from flask import request
from flocx_market.objects import offer_contract_relationship as ocr


class OfferContractRelationship(Resource):

    @classmethod
    def get(cls, marketplace_offer_id=None, contract_id=None):
        if (contract_id is None) and (marketplace_offer_id is None):
            return [x.to_dict() for x in
                    ocr.OfferContractRelationship.get_all()]
        ocrs = ocr.OfferContractRelationship.get(marketplace_offer_id,
                                                 contract_id)
        if ocrs is None:
            return {'message': 'OfferContractRelationship not found'}, 404

        if (marketplace_offer_id is not None) and (contract_id is not None):
            return ocrs.to_dict()
        else:
            return [a.to_dict() for a in ocrs]

    @classmethod
    def delete(cls, contract_id, marketplace_offer_id):
        o = ocr.OfferContractRelationship.get(contract_id,
                                              marketplace_offer_id)
        if o is None:
            return {'message': 'OfferContractRelationship not found.'}, 404
        o.destroy()
        return {'message': 'OfferContractRelationship deleted.'}

    @classmethod
    def put(cls, contract_id, marketplace_offer_id):
        data = request.get_json(force=True)
        o = ocr.OfferContractRelationship.get(contract_id,
                                              marketplace_offer_id)
        if o is None:
            return {'message': 'OfferContractRelationship not found.'}, 404
        # we only allow status field to be modified
        if 'status' in data:
            o.status = data['status']
            return o.save().to_dict()
        return o.to_dict()
