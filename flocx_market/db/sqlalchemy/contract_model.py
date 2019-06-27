from flocx_market.db.orm import orm


class ContractModel(orm.Model):
    __tablename__ = 'contracts'
    contract_id = orm.Column(orm.String(64), primary_key=True, autoincrement=False)
    time_created = orm.Column(orm.DateTime(timezone=True), nullable=False)
    status = orm.Column(orm.String(15), nullable=False, default='available')
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)

    bid_id = orm.Column(orm.String(64), orm.ForeignKey('bids.marketplace_bid_id'))
    bid = orm.relationship('BidModel')

    offers = orm.relationship('OfferModel', lazy='dynamic')
