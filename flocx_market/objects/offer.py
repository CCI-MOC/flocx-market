from oslo_versionedobjects import base as versioned_objects_base
import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields
from flocx_market.objects import offer_contract_relationship as ocr
from flocx_market.objects import contract


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

    @classmethod
    def get_available_status_contract(cls,
                                      context,
                                      start_time,
                                      end_time):
        def check_contracts_time(context,
                                 prev_contracts,
                                 start_time,
                                 end_time):
            for con in prev_contracts:
                c = contract.Contract.get(con.contract_id, context)
                if not (end_time <= c.start_time or start_time >= c.end_time):
                    return False
            return True

        offers_by_status = db.offer_get_all_by_status('available', context)

        if start_time is None and end_time is None:
            return cls._from_db_object_list(offers_by_status)

        else:
            valid_offers = []
            for o in offers_by_status:
                prev_con = ocr.OfferContractRelationship. \
                    get_all(context,
                            filters={'marketplace_offer_id':
                                     o.marketplace_offer_id}
                            )

                if o.start_time < start_time and o.end_time > end_time \
                        and check_contracts_time(context, prev_con,
                                                 start_time,
                                                 end_time):
                    valid_offers.append(o)

            return cls._from_db_object_list(valid_offers)

    @classmethod
    def get_all_by_status(cls, status, context):
        available = db.offer_get_all_by_status(status, context)
        return cls._from_db_object_list(available)
