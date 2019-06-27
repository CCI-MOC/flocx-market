from flocx_market.db.orm import orm
import sqlalchemy_jsonfield


class OfferModel(orm.Model):
    __tablename__ = 'offers'
    marketplace_offer_id = orm.Column(orm.String(64), primary_key=True, autoincrement=False)
    provider_id = orm.Column(orm.String(64), nullable=False)
    creator_id = orm.Column(orm.String(64), nullable=False)
    marketplace_date_created = orm.Column(orm.DateTime(timezone=True), nullable=False)
    status = orm.Column(orm.String(15), nullable=False, default='available')
    server_id = orm.Column(orm.String(64), nullable=False, unique=True)
    start_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    end_time = orm.Column(orm.DateTime(timezone=True), nullable=False)
    server_config = orm.Column(sqlalchemy_jsonfield.JSONField(enforce_string=True, enforce_unicode=False), nullable=False)
    cost = orm.Column(orm.Float, nullable=False)

    contract_id = orm.Column(orm.String(64), orm.ForeignKey('contracts.contract_id'), nullable=True)
    contract = orm.relationship('ContractModel')
