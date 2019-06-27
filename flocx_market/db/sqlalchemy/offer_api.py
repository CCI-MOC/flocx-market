from flocx_market.db.orm import orm
from flocx_market.db.sqlalchemy.offer_model import OfferModel
from uuid import uuid4


class OfferApi(OfferModel):
    def __init__(self, provider_id, creator_id, marketplace_date_created, status, server_id, start_time, end_time, server_config, cost):
        self.marketplace_offer_id = str(uuid4())
        self.provider_id = provider_id
        self.creator_id = creator_id
        self.marketplace_date_created = marketplace_date_created
        self.status = status
        self.server_id = server_id
        self.start_time = start_time
        self.end_time = end_time
        self.server_config = server_config
        self.cost = cost

    def as_dict(self):
        d = {}
        for col in self.__table__.columns:
            if col.name in ['marketplace_date_created', 'start_time', 'end_time']:
                d[col.name] = getattr(self, col.name).isoformat()
            else:
                d[col.name] = getattr(self, col.name)
        return d

    @classmethod
    def find_by_id(cls, marketplace_offer_id):
        return cls.query.filter_by(marketplace_offer_id=marketplace_offer_id).first()

    def save_to_db(self):
        orm.session.add(self)
        orm.session.commit()

    def delete_from_db(self):
        orm.session.delete(self)
        orm.session.commit()
