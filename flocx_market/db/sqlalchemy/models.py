from flocx_market.db.orm import orm
import sqlalchemy_jsonfield


class Offer(orm.Model):
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


class Bid(orm.Model):
    __tablename__ = 'bids'
    marketplace_bid_id = orm.Column(
        orm.String(64),
        primary_key=True,
        autoincrement=False,
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

    def to_dict(self):
        d = {}
        for col in self.__table__.columns:
            if col.name in ['start_time', 'end_time']:
                d[col.name] = getattr(self, col.name).isoformat()
            else:
                d[col.name] = getattr(self, col.name)
        return d
