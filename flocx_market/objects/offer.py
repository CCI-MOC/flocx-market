from oslo_versionedobjects import base as versioned_objects_base

import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields


@versioned_objects_base.VersionedObjectRegistry.register
class Offer(base.FLOCXMarketObject):

    fields = {
        'marketplace_offer_id': fields.StringField(),
        'provider_offer_id': fields.StringField(),
        'provider_id': fields.StringField(),
        'marketplace_date_created': fields.DateTimeField(nullable=True),
        'status': fields.StringField(),
        'server_id': fields.StringField(),
        'start_time': fields.DateTimeField(nullable=True),
        'end_time': fields.DateTimeField(nullable=True),
        'server_config': fields.FlexibleDictField(nullable=True),
        'cost': fields.FloatField(),
        'project_id': fields.StringField()
    }

    @classmethod
    def create(cls, data):
        o = db.offer_create(data)
        return cls._from_db_object(cls(), o)

    @classmethod
    def get(cls, offer_id):
        if offer_id is None:
            return None
        else:
            o = db.offer_get(offer_id)
            if o is None:
                return None
            else:
                return cls._from_db_object(cls(), o)

    def destroy(self):
        db.offer_destroy(self.marketplace_offer_id)
        return True

    @classmethod
    def get_all(cls):
        all_offers = db.offer_get_all()
        return cls._from_db_object_list(all_offers)

    def save(self):
        updates = self.obj_get_changes()
        db_offer = db.offer_update(
            self.marketplace_offer_id, updates)
        return self._from_db_object(self, db_offer)

    @classmethod
    def get_all_unexpired(cls):
        unexpired = db.offer_get_all_unexpired()
        return cls._from_db_object_list(unexpired)

    def expire(self):
        self.status = 'expired'
        self.save()
