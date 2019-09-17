import datetime
from oslo_versionedobjects import base as versioned_objects_base

from flocx_market.common import statuses
import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields
from flocx_market.objects import offer_contract_relationship


@versioned_objects_base.VersionedObjectRegistry.register
class Contract(base.FLOCXMarketObject):

    fields = {
        'contract_id': fields.StringField(),
        'status': fields.StringField(),
        'start_time': fields.DateTimeField(nullable=True),
        'end_time': fields.DateTimeField(nullable=True),
        'cost': fields.FloatField(),
        'bid_id': fields.StringField(),
        'project_id': fields.StringField()
    }

    def to_dict(self):
        ret = dict()
        for k in self.fields:
            val = getattr(self, k)
            if type(val) == datetime.datetime:
                ret[k] = val.isoformat()
            elif k == 'bid' and val is None:
                continue
            else:
                ret[k] = val
        return ret

    @classmethod
    def get(cls, contract_id, context):
        if contract_id is None:
            return None
        else:
            c = db.contract_get(contract_id, context)
            if c is None:
                return None
            else:
                return cls._from_db_object(cls(), c)

    @classmethod
    def get_all(cls, context):
        all_contracts = db.contract_get_all(context)
        return cls._from_db_object_list(all_contracts)

    @classmethod
    def get_all_by_status(cls, context, status):
        contracts = db.contract_get_all_by_status(context, status)
        return cls._from_db_object_list(contracts)

    @classmethod
    def create(cls, data, context):
        c = db.contract_create(data, context)
        return cls._from_db_object(cls(), c)

    def destroy(self, context):
        db.contract_destroy(self.contract_id, context)
        return True

    def save(self, context):
        updates = self.obj_get_changes()
        db_contract = db.contract_update(self.contract_id, updates, context)
        return self._from_db_object(self, db_contract)

    @classmethod
    def get_all_unexpired(cls, context):
        unexpired = db.contract_get_all_unexpired(context)
        return cls._from_db_object_list(unexpired)

    def fulfill(self, context):
        ocrs = offer_contract_relationship.OfferContractRelationship.get_all(
            context, {'contract_id': self.contract_id})
        for ocr in ocrs:
            ocr.fulfill(context)

        self.status = statuses.FULFILLED
        self.save(context)

    def expire(self, context):
        ocrs = offer_contract_relationship.OfferContractRelationship.get_all(
            context, {'contract_id': self.contract_id})
        for ocr in ocrs:
            ocr.expire(context)

        self.status = statuses.EXPIRED
        self.save(context)
