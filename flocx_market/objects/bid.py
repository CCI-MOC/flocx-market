import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields


class Bid(base.FLOCXMarketObject):

    fields = {
        'marketplace_bid_id': fields.StringField(),
        'creator_bid_id': fields.StringField(),
        'creator_id': fields.StringField(),
        'server_quantity': fields.IntegerField(),
        'start_time': fields.DateTimeField(nullable=True),
        'end_time': fields.DateTimeField(nullable=True),
        'duration': fields.IntegerField(),
        'status': fields.StringField(),
        'server_config_query': fields.FlexibleDictField(nullable=True),
        'cost': fields.FloatField()
    }

    @classmethod
    def create(cls, data):
        b = db.bid_create(data)
        return cls._from_db_object(cls(), b)

    @classmethod
    def get(cls, bid_id):
        if bid_id is None:
            return None
        else:
            b = db.bid_get(bid_id)
            if b is None:
                return None
            else:
                return cls._from_db_object(cls(), b)

    def destroy(cls):
        db.bid_destroy(cls.marketplace_bid_id)
        return True

    @classmethod
    def get_all(cls):
        all_bids = db.bid_get_all()
        return cls._from_db_object_list(all_bids)

    def save(cls, data):
        cls.status = data['status']
        db.bid_update(cls.marketplace_bid_id, data)
        return cls
