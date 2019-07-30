from oslo_versionedobjects import base as versioned_objects_base

import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields


@versioned_objects_base.VersionedObjectRegistry.register
class Bid(base.FLOCXMarketObject):

    fields = {
        'marketplace_bid_id': fields.StringField(),
        'project_id': fields.StringField(),
        'server_quantity': fields.IntegerField(),
        'start_time': fields.DateTimeField(nullable=True),
        'end_time': fields.DateTimeField(nullable=True),
        'duration': fields.IntegerField(),
        'status': fields.StringField(),
        'server_config_query': fields.FlexibleDictField(nullable=True),
        'cost': fields.FloatField(),
    }

    @classmethod
    def create(cls, data, context):
        b = db.bid_create(data, context)
        return cls._from_db_object(cls(), b)

    @classmethod
    def get(cls, bid_id, context):
        if bid_id is None:
            return None
        else:
            b = db.bid_get(bid_id, context)
            if b is None:
                return None
            else:
                return cls._from_db_object(cls(), b)

    def destroy(self, context):
        db.bid_destroy(self.marketplace_bid_id, context)
        return True

    @classmethod
    def get_all(cls, context):
        all_bids = db.bid_get_all(context)
        return cls._from_db_object_list(all_bids)

    def save(self, context):
        updates = self.obj_get_changes()
        db_bid = db.bid_update(
            self.marketplace_bid_id, updates, context)
        return self._from_db_object(self, db_bid)

    @classmethod
    def get_all_unexpired(cls, context):
        unexpired = db.bid_get_all_unexpired(context)
        return cls._from_db_object_list(unexpired)

    @classmethod
    def get_all_by_project_id(cls, context):
        by_project_id = db.bid_get_all_by_project_id(context)
        return cls._from_db_object_list(by_project_id)

    def expire(self, context):
        self.status = 'expired'
        self.save(context)
