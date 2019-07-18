import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields


class Offer(base.FLOCXMarketObject):

    fields = {
        'marketplace_offer_id': fields.StringField(),
        'provider_id': fields.StringField(),
        'creator_id': fields.StringField(),
        'marketplace_date_created': fields.DateTimeField(nullable=True),
        'status': fields.StringField(),
        'server_id': fields.StringField(),
        'start_time': fields.DateTimeField(nullable=True),
        'end_time': fields.DateTimeField(nullable=True),
        'server_config': fields.FlexibleDictField(nullable=True),
        'cost': fields.FloatField()
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

    def destroy(cls):
        db.offer_destroy(cls.marketplace_offer_id)
        return True

    @classmethod
    def get_all(cls):
        all_offers = db.offer_get_all()
        return cls._from_db_object_list(all_offers)

    def save(cls, data):
        cls.status = data['status']
        db.offer_update(cls.marketplace_offer_id, data)
        return cls
