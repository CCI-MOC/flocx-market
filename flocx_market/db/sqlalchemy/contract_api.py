from flocx_market.db.orm import orm
from flocx_market.db.sqlalchemy.offer_api import OfferApi
from flocx_market.db.sqlalchemy.contract_model import ContractModel
from uuid import uuid4


class ContractApi(ContractModel):
    def __init__(self, time_created, bid_id, status, start_time, end_time, cost, offers):
        self.contract_id = str(uuid4())
        self.time_created = time_created
        self.bid_id = bid_id
        self.status = status
        self.start_time = start_time
        self.end_time = end_time
        self.cost = cost

    def as_dict(self):
        d = {}
        for col in self.__table__.columns:
            if col.name in ['time_created', 'start_time', 'end_time']:
                d[col.name] = getattr(self, col.name).isoformat()
            else:
                d[col.name] = getattr(self, col.name)
        offer_model_objects = [offer for offer in self.offers.all()]

        # needed to avoid foreign key constraint issue since model and api are separated
        offer_api_objects = []
        for o in offer_model_objects:
            for i in o.__table__.columns:
                if i.name == "marketplace_offer_id":
                    offer_api_obj = OfferApi.find_by_id(getattr(o, i.name))
                    offer_api_objects.append(offer_api_obj)

        if offer_api_objects:
            d["offers"] = [offer.as_dict() for offer in offer_api_objects]
        return d

    @classmethod
    def find_by_id(cls, contract_id):
        return cls.query.filter_by(contract_id=contract_id).first()

    def save_to_db(self):
        orm.session.add(self)
        orm.session.commit()

    def delete_from_db(self):
        orm.session.delete(self)
        orm.session.commit()
