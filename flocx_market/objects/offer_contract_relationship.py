from oslo_versionedobjects import base as versioned_objects_base

import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields


@versioned_objects_base.VersionedObjectRegistry.register
class OfferContractRelationship(base.FLOCXMarketObject):

    fields = {
        'offer_contract_relationship_id': fields.StringField(),
        'marketplace_offer_id': fields.StringField(),
        'contract_id': fields.StringField(),
        'status': fields.StringField(),
    }

    @classmethod
    def get(cls, context, contract_id, marketplace_offer_id):
        if (contract_id is None) and (marketplace_offer_id is None):
            return None
        else:
            o = db.offer_contract_relationship_get(
                contract_id=contract_id,
                marketplace_offer_id=marketplace_offer_id,
                context=context)
            if o is None:
                return None
            else:
                return cls._from_db_object(cls(), o)

    def destroy(self, context):
        db.offer_contract_relationship_destroy(
            contract_id=self.contract_id,
            marketplace_offer_id=self.marketplace_offer_id,
            context=context)
        return True

    @classmethod
    def get_all(cls, context):
        all_ocrs = db.offer_contract_relationship_get_all(context)
        return cls._from_db_object_list(all_ocrs)

    def save(self, context):
        updates = self.obj_get_changes()
        db_offer_contract_relationship = db.offer_contract_relationship_update(
            context,
            self.contract_id,
            self.marketplace_offer_id,
            updates,
            )
        return self._from_db_object(self, db_offer_contract_relationship)

    @classmethod
    def get_all_unexpired(cls, context):
        unexpired = db.offer_contract_relationship_get_all_unexpired(context)
        return cls._from_db_object_list(unexpired)

    def expire(self, context):
        self.status = 'expired'
        self.save(context)
