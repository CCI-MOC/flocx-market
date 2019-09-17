from oslo_db.sqlalchemy import models
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_jsonfield
import datetime

from flocx_market.common import statuses
from flocx_market.db.orm import orm
from flocx_market.resource_objects import resource_types


class FLOCXMarketBase(models.TimestampMixin, models.ModelBase):
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
    bid_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    project_id = orm.Column(orm.String(64), nullable=False)
    quantity = orm.Column(orm.Integer, nullable=False)
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    duration = orm.Column(orm.Integer, nullable=False)
    status = orm.Column(
        orm.String(15), nullable=False, default=statuses.AVAILABLE)
    config_query = orm.Column(sqlalchemy_jsonfield.JSONField(
        enforce_string=True,
        enforce_unicode=False), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)
    contracts = orm.relationship('Contract', lazy='dynamic')

    @orm.validates('cost')
    def validate_cost(self, key, value):
        if value < 0:
            raise ValueError('Cost must be >= 0')
        return value


class Offer(Base):
    __tablename__ = "offers"
    offer_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    project_id = orm.Column(orm.String(64), nullable=False)
    status = orm.Column(
        orm.String(15), nullable=False, default=statuses.AVAILABLE)
    resource_id = orm.Column(orm.String(64), nullable=False)
    resource_type = orm.Column(
        orm.String(64), nullable=False, default=resource_types.IRONIC_NODE)
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=True)
    config = orm.Column(
        sqlalchemy_jsonfield.JSONField(enforce_string=True,
                                       enforce_unicode=False),
        nullable=False,
    )
    cost = orm.Column(orm.Float, nullable=False)
    offer_contract_relationships = orm.relationship(
        'OfferContractRelationship', lazy='dynamic')

    @orm.validates('cost')
    def validate_cost(self, key, value):
        if value < 0:
            raise ValueError('Cost must be >= 0')
        return value


class Contract(Base):
    __tablename__ = 'contracts'
    contract_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    status = orm.Column(
        orm.String(15), nullable=False, default=statuses.AVAILABLE)
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)
    bid_id = orm.Column(orm.String(64),
                        orm.ForeignKey('bids.bid_id'))
    bid = orm.relationship('Bid')
    offer_contract_relationships = orm.relationship(
        'OfferContractRelationship', lazy='dynamic')
    project_id = orm.Column(orm.String(64), nullable=False)


class OfferContractRelationship(Base):
    __tablename__ = 'offer_contract_relationship'
    offer_contract_relationship_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    offer_id = orm.Column(
        orm.String(64), orm.ForeignKey('offers.offer_id'))
    offer = orm.relationship('Offer')
    contract_id = orm.Column(orm.String(64),
                             orm.ForeignKey('contracts.contract_id'))
    contract = orm.relationship('Contract')
    status = orm.Column(
        orm.String(15), nullable=False, default=statuses.AVAILABLE)
