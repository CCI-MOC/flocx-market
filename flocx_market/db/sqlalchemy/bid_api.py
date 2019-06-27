from flocx_market.db.orm import orm
from flocx_market.db.sqlalchemy.bid_model import BidModel
from uuid import uuid4


class BidApid(BidModel):
    def __init__(self, creator_bid_id, creator_id, server_quantity, start_time, end_time, duration, status, server_config_query, cost):
        self.marketplace_bid_id = str(uuid4())
        self.creator_bid_id = creator_bid_id
        self.creator_id = creator_id
        self.server_quantity = server_quantity
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.status = status
        self.server_config_query = server_config_query
        self.cost = cost

    def as_dict(self):
        d = {}
        for col in self.__table__.columns:
            if col.name in ['start_time', 'end_time']:
                d[col.name] = getattr(self, col.name).isoformat()
            else:
                d[col.name] = getattr(self, col.name)
        return d

    @classmethod
    def find_by_id(cls, marketplace_bid_id):
        return cls.query.filter_by(marketplace_bid_id=marketplace_bid_id).first()

    def save_to_db(self):
        orm.session.add(self)
        orm.session.commit()

    def delete_from_db(self):
        orm.session.delete(self)
        orm.session.commit()
