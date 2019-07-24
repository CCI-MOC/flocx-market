from oslo_db.sqlalchemy import models
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_jsonfield
import datetime

from flocx_market.db.orm import orm


class FLOCXMarketBase(models.ModelBase):
    metadata = None

    def to_dict(self):
        d = {}
        for col in self.__table__.columns:
            val = getattr(self, col.name)
            if type(val) == datetime.datetime:
                d[col.name] = val.isoformat()
            else:
                d[col.name] = val
        return d


Base = declarative_base(cls=FLOCXMarketBase)


class Bid(Base):
    __tablename__ = 'bids'
    marketplace_bid_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    creator_bid_id = orm.Column(orm.String(64), nullable=False)
    server_quantity = orm.Column(orm.Integer, nullable=False)
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    duration = orm.Column(orm.Integer, nullable=False)
    status = orm.Column(orm.String(15), nullable=False, default='available')
    server_config_query = orm.Column(sqlalchemy_jsonfield.JSONField(
        enforce_string=True,
        enforce_unicode=False), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)
    contracts = orm.relationship('Contract', lazy='dynamic')
    project_id = orm.Column(orm.String(64), nullable=False)


class Offer(Base):
    __tablename__ = "offers"
    marketplace_offer_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    provider_offer_id = orm.Column(
        orm.String(64),
        nullable=False,
        unique=True,
    )
    provider_id = orm.Column(orm.String(64), nullable=False)
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
    contract_id = orm.Column(orm.String(64),
                             orm.ForeignKey('contracts.contract_id'),
                             nullable=True)
    contract = orm.relationship('Contract')
    project_id = orm.Column(orm.String(64), nullable=False)


class Contract(Base):
    __tablename__ = 'contracts'
    contract_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    time_created = orm.Column(orm.DateTime(timezone=True), nullable=False)
    status = orm.Column(orm.String(15), nullable=False, default='available')
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)
    bid_id = orm.Column(orm.String(64),
                        orm.ForeignKey('bids.marketplace_bid_id'))
    bid = orm.relationship('Bid')
    offers = orm.relationship('Offer', lazy='dynamic')
    project_id = orm.Column(orm.String(64), nullable=False)
