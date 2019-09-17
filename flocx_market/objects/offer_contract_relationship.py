from oslo_versionedobjects import base as versioned_objects_base

from flocx_market.common import statuses
import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import contract
from flocx_market.objects import fields
from flocx_market.objects import offer


@versioned_objects_base.VersionedObjectRegistry.register
class OfferContractRelationship(base.FLOCXMarketObject):

    fields = {
        'offer_contract_relationship_id': fields.StringField(),
        'offer_id': fields.StringField(),
        'contract_id': fields.StringField(),
        'status': fields.StringField(),
    }

    @classmethod
    def get(cls, context, ocr_id):
        o = db.offer_contract_relationship_get(context, ocr_id)
        if o is None:
            return None
        else:
            return cls._from_db_object(cls(), o)

    def destroy(self, context):
        db.offer_contract_relationship_destroy(
            context,
            self.offer_contract_relationship_id)
        return True

    @classmethod
    def get_all(cls, context, filters=None):

        o = db.offer_contract_relationship_get_all(context, filters)

        return cls._from_db_object_list(o)

    def save(self, context):
        updates = self.obj_get_changes()
        db_offer_contract_relationship = db.offer_contract_relationship_update(
            context, self.offer_contract_relationship_id, updates)
        return self._from_db_object(self, db_offer_contract_relationship)

    def contract(self, context):
        return contract.Contract.get(self.contract_id, context)

    def offer(self, context):
        return offer.Offer.get(self.offer_id, context)

    @classmethod
    def get_all_unexpired(cls, context):
        unexpired = db.offer_contract_relationship_get_all_unexpired(context)
        return cls._from_db_object_list(unexpired)

    def fulfill(self, context):
        ro = self.offer(context).resource_object()
        ro.set_contract(self.contract(context))

        self.status = statuses.FULFILLED
        self.save(context)

    def expire(self, context):
        ro = self.offer(context).resource_object()
        c = self.contract(context)
        if ro.get_contract_uuid() == c.contract_id:
            ro.set_contract(None)

        self.status = statuses.EXPIRED
        self.save(context)
