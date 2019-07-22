from oslo_versionedobjects import base as versioned_objects_base
import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields
import datetime


@versioned_objects_base.VersionedObjectRegistry.register
class Contract(base.FLOCXMarketObject):

    fields = {
        'contract_id': fields.StringField(),
        'time_created': fields.DateTimeField(nullable=True),
        'status': fields.StringField(),
        'start_time': fields.DateTimeField(nullable=True),
        'end_time': fields.DateTimeField(nullable=True),
        'cost': fields.FloatField(),
        'bid_id': fields.StringField(),
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
    def get(cls, contract_id):
        if contract_id is None:
            return None
        else:
            c = db.contract_get(contract_id)
            if c is None:
                return None
            else:
                return cls._from_db_object(cls(), c)

    @classmethod
    def get_all(cls):
        all_contracts = db.contract_get_all()
        return cls._from_db_object_list(all_contracts)

    @classmethod
    def create(cls, data):
        c = db.contract_create(data)
        return cls._from_db_object(cls(), c)

    def destroy(self):
        db.contract_destroy(self.contract_id)
        return True

    def save(self):
        updates = self.obj_get_changes()
        db_contract = db.contract_update(self.contract_id, updates)
        return self._from_db_object(self, db_contract)

    @classmethod
    def get_all_unexpired(cls):
        unexpired = db.contract_get_all_unexpired()
        return cls._from_db_object_list(unexpired)

    def expire(self):
        self.status = 'expired'
        self.save()
