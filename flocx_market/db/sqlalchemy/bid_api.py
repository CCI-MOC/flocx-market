from flocx_market.db.orm import orm
from flocx_market.db.sqlalchemy.bid_model import BidModel


class BidApi(BidModel):

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
        return cls.query.filter_by(
            marketplace_bid_id=marketplace_bid_id).first()

    def save_to_db(self):
        orm.session.add(self)
        orm.session.commit()

    def delete_from_db(self):
        orm.session.delete(self)
        orm.session.commit()
