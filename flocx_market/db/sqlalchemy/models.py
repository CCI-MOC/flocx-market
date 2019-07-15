from oslo_db.sqlalchemy import models
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_jsonfield

from flocx_market.db.orm import orm


class FLOCXMarketBase(models.ModelBase):

    metadata = None

    def to_dict(self):
        d = {}
        for col in self.__table__.columns:
            if col.name in [
                    'marketplace_date_created', 'start_time', 'end_time'
            ]:
                d[col.name] = getattr(self, col.name).isoformat()
            else:
                d[col.name] = getattr(self, col.name)
        return d


Base = declarative_base(cls=FLOCXMarketBase)


class Offer(Base):
    __tablename__ = "offers"
    marketplace_offer_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    provider_id = orm.Column(orm.String(64), nullable=False)
    creator_id = orm.Column(orm.String(64), nullable=False)
    marketplace_date_created = orm.Column(orm.DateTime(timezone=True),
                                          nullable=False)
    status = orm.Column(orm.String(15), nullable=False, default="available")
    server_id = orm.Column(orm.String(64), nullable=False, unique=True)
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    server_config = orm.Column(
        sqlalchemy_jsonfield.JSONField(enforce_string=True,
                                       enforce_unicode=False),
        nullable=False,
    )
    cost = orm.Column(orm.Float, nullable=False)
