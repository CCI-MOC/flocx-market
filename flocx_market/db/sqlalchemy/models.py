from oslo_db.sqlalchemy import models
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy_jsonfield
import datetime

from flocx_market.db.orm import orm
import flocx_market.common.exception as e


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
    marketplace_bid_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
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
            raise e.InvalidInput('Cost must be >= 0')
        return value

    @orm.validates('server_config_query')
    def validate_server_config_query(self, key, value):
        if type(value) is not dict:
            raise e.InvalidInput('server_config_query must be a dictionary')
        if 'specs' not in value:
            raise e.InvalidInput("server_config_query must contain key \
                                    'specs'")
        return value

    @orm.validates('start_time', 'end_time')
    def validate_start_end_times(self, key, value):

        time = value
        if not isinstance(time, datetime.datetime):
            time = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

        if key == 'end_time':
            if time < self.start_time:
                raise e.InvalidInput('start_time must be before end_time')

        return time


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
    project_id = orm.Column(orm.String(64), nullable=False)
    status = orm.Column(orm.String(15), nullable=False, default="available")
    server_id = orm.Column(orm.String(64), nullable=False)
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
            raise e.InvalidInput('Cost must be >= 0')
        return value

    @orm.validates('server_config')
    def validate_server_config(self, key, value):
        if type(value) is not dict:
            raise e.InvalidInput('server_config must be a dictionary')
        return value

    @orm.validates('start_time', 'end_time')
    def validate_start_end_times(self, key, value):

        time = value
        if not isinstance(time, datetime.datetime):
            time = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

        if key == 'end_time':
            if time < self.start_time:
                raise e.InvalidInput('start_time must be before end_time')

        return time


class Contract(Base):
    __tablename__ = 'contracts'
    contract_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    status = orm.Column(orm.String(15), nullable=False, default='unretrieved')
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)
    bid_id = orm.Column(orm.String(64),
                        orm.ForeignKey('bids.marketplace_bid_id'))
    bid = orm.relationship('Bid')
    offer_contract_relationships = orm.relationship(
        'OfferContractRelationship', lazy='dynamic')
    project_id = orm.Column(orm.String(64), nullable=False)

    @orm.validates('start_time', 'end_time')
    def validate_start_end_times(self, key, value):

        time = value
        if not isinstance(time, datetime.datetime):
            time = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')

        if key == 'end_time':
            if time < self.start_time:
                raise e.InvalidInput('start_time must be before end_time')

        return time


class OfferContractRelationship(Base):
    __tablename__ = 'offer_contract_relationship'
    offer_contract_relationship_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
    )
    marketplace_offer_id = orm.Column(
        orm.String(64), orm.ForeignKey('offers.marketplace_offer_id'))
    marketplace_offer = orm.relationship('Offer')
    contract_id = orm.Column(orm.String(64),
                             orm.ForeignKey('contracts.contract_id'))
    contract = orm.relationship('Contract')
    status = orm.Column(orm.String(15), nullable=False, default='available')
