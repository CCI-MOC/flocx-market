from oslo_versionedobjects import base as versioned_objects_base

from flocx_market.common import statuses
import flocx_market.db.sqlalchemy.api as db
from flocx_market.objects import base
from flocx_market.objects import fields
from flocx_market.objects import offer_contract_relationship as oc_relationship
from flocx_market.objects import contract
from flocx_market.resource_objects import resource_object_factory as ro_factory


@versioned_objects_base.VersionedObjectRegistry.register
class Offer(base.FLOCXMarketObject):

    fields = {
        'offer_id': fields.StringField(),
        'project_id': fields.StringField(),
        'status': fields.StringField(),
        'resource_id': fields.StringField(),
        'resource_type': fields.StringField(),
        'start_time': fields.DateTimeField(nullable=True),
        'end_time': fields.DateTimeField(nullable=True),
        'config': fields.FlexibleDictField(nullable=True),
        'cost': fields.FloatField(),
    }

    @classmethod
    def create(cls, data, context):
        if 'config' not in data:
            ro = ro_factory.ResourceObjectFactory.get_resource_object(
                data['resource_type'], data['resource_id'])
            data['config'] = ro.get_node_config()

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
        db.offer_destroy(self.offer_id, context)
        return True

    @classmethod
    def get_all(cls, context):
        all_offers = db.offer_get_all(context)
        return cls._from_db_object_list(all_offers)

    def save(self, context):
        updates = self.obj_get_changes()
        db_offer = db.offer_update(
            self.offer_id, updates, context)
        return self._from_db_object(self, db_offer)

    @classmethod
    def get_all_unexpired(cls, context):
        unexpired = db.offer_get_all_unexpired(context)
        return cls._from_db_object_list(unexpired)

    @classmethod
    def get_all_by_project_id(cls, context):
        by_project_id = db.offer_get_all_by_project_id(context)
        return cls._from_db_object_list(by_project_id)

    def related_contracts(self, context):
        related_contracts = []
        ocrs = oc_relationship.OfferContractRelationship.get_all(
            context,
            {'offer_id': self.offer_id}
        )
        for ocr in ocrs:
            related_contracts.append(ocr.contract(context))
        return related_contracts

    def expire(self, context):
        # make sure all related contracts are expired
        related_contracts = self.related_contracts(context)
        for c in related_contracts:
            if c.status != statuses.EXPIRED:
                c.expire(context)

        self.status = statuses.EXPIRED
        self.save(context)

    def resource_object(self):
        return ro_factory.ResourceObjectFactory.get_resource_object(
            self.resource_type, self.resource_id)

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

        offers_by_status = db.offer_get_all_by_status(
            statuses.AVAILABLE, context)

        if start_time is None and end_time is None:
            return cls._from_db_object_list(offers_by_status)

        else:
            valid_offers = []
            for o in offers_by_status:
                prev_con = oc_relationship.OfferContractRelationship. \
                    get_all(context,
                            filters={'offer_id':
                                     o.offer_id}
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
