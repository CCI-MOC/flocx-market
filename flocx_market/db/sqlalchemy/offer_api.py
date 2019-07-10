from flocx_market.db.orm import orm
from flocx_market.db.sqlalchemy.offer_model import OfferModel
from uuid import uuid4
import json


class OfferApi(OfferModel):
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
