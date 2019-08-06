from oslo_db.sqlalchemy import models
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_jsonfield
import datetime

from flocx_market.db.orm import orm


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

    id = orm.Column(orm.Integer, primary_key=True, autoincrement=True)
    marketplace_bid_id = orm.Column(orm.String(64))
    project_id = orm.Column(orm.String(64), nullable=False)
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

    @orm.validates('cost')
    def validate_cost(self, key, value):
        if value < 0:
            raise ValueError('Cost must be >= 0')
        return value


class Offer(Base):
    __tablename__ = "offers"

    id = orm.Column(orm.Integer, primary_key=True, autoincrement=True)
    marketplace_offer_id = orm.Column(orm.String(64))
    provider_offer_id = orm.Column(
        orm.String(64),
        nullable=False,
        unique=True,
    )
    project_id = orm.Column(orm.String(64), nullable=False)
    status = orm.Column(orm.String(15), nullable=False, default="available")
    server_id = orm.Column(orm.String(64), nullable=False, unique=True)
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=True)
    server_config = orm.Column(
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

    id = orm.Column(orm.Integer, primary_key=True, autoincrement=True)
    contract_id = orm.Column(orm.String(64))
    status = orm.Column(orm.String(15), nullable=False, default='unretrieved')
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)
    bid_id = orm.Column(orm.Integer,
                        orm.ForeignKey('bids.id'))
    bid = orm.relationship('Bid')
    offer_contract_relationships = orm.relationship(
        'OfferContractRelationship', lazy='dynamic')
    project_id = orm.Column(orm.String(64), nullable=False)


class OfferContractRelationship(Base):
    __tablename__ = 'offer_contract_relationship'

    id = orm.Column(orm.Integer, primary_key=True, autoincrement=True)
    offer_contract_relationship_id = orm.Column(orm.String(64))
    marketplace_offer_id = orm.Column(orm.Integer,
                                      orm.ForeignKey('offers.id'))
    marketplace_offer = orm.relationship('Offer')
    contract_id = orm.Column(orm.Integer,
                             orm.ForeignKey('contracts.id'))
    contract = orm.relationship('Contract')
    status = orm.Column(orm.String(15), nullable=False, default='available')
