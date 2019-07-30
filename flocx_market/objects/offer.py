from oslo_versionedobjects import base as versioned_objects_base

import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields


@versioned_objects_base.VersionedObjectRegistry.register
class Offer(base.FLOCXMarketObject):

    fields = {
        'marketplace_offer_id': fields.StringField(),
        'provider_offer_id': fields.StringField(),
        'project_id': fields.StringField(),
        'status': fields.StringField(),
        'server_id': fields.StringField(),
        'start_time': fields.DateTimeField(nullable=True),
        'end_time': fields.DateTimeField(nullable=True),
        'server_config': fields.FlexibleDictField(nullable=True),
        'cost': fields.FloatField(),
    }

    @classmethod
    def create(cls, data, context):
        o = db.offer_create(data, context)
        return cls._from_db_object(cls(), o)

    @classmethod
    def get(cls, offer_id, context):
        if offer_id is None:
            return None
        else:
            o = db.offer_get(offer_id, context)
            if o is None:
                return None
            else:
                return cls._from_db_object(cls(), o)

    def destroy(self, context):
        db.offer_destroy(self.marketplace_offer_id, context)
        return True

    @classmethod
    def get_all(cls, context):
        all_offers = db.offer_get_all(context)
        return cls._from_db_object_list(all_offers)

    def save(self, context):
        updates = self.obj_get_changes()
        db_offer = db.offer_update(
            self.marketplace_offer_id, updates, context)
        return self._from_db_object(self, db_offer)

    @classmethod
    def get_all_unexpired(cls, context):
        unexpired = db.offer_get_all_unexpired(context)
        return cls._from_db_object_list(unexpired)

    @classmethod
    def get_all_by_project_id(cls, context):
        by_project_id = db.offer_get_all_by_project_id(context)
        return cls._from_db_object_list(by_project_id)

    def expire(self, context):
        self.status = 'expired'
        self.save(context)
