import uuid

from flocx_market.db.orm import orm
import sqlalchemy_jsonfield


class BidModel(orm.Model):
    __tablename__ = 'bids'
    marketplace_bid_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
        default=lambda: uuid.uuid4().hex,
    )
    creator_bid_id = orm.Column(orm.String(64), nullable=False)
    creator_id = orm.Column(orm.String(64), nullable=False)
    server_quantity = orm.Column(orm.Integer, nullable=False)
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    duration = orm.Column(orm.Integer, nullable=False)
    status = orm.Column(orm.String(15), nullable=False, default='available')
    server_config_query = orm.Column(sqlalchemy_jsonfield.JSONField(
                                     enforce_string=True,
                                     enforce_unicode=False), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)
