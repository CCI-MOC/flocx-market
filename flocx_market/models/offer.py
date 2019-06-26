from flocx_market.db import db
import sqlalchemy_jsonfield

class OfferModel(db.Model):
    __tablename__ = 'offers'
    marketplace_offer_id = db.Column(db.String(64), primary_key=True, autoincrement=False)
    provider_id = db.Column(db.String(64), nullable=False)
    creator_id = db.Column(db.String(64), nullable=False) #username that created the offer
    marketplace_date_created = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.String(15), nullable=False, default = 'available')
    server_id = db.Column(db.String(64), nullable=False, unique=True)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    server_config = db.Column(sqlalchemy_jsonfield.JSONField(enforce_string=True,enforce_unicode=False), nullable=False)
    cost = db.Column(db.Float, nullable=False)

    def __init__(self, marketplace_offer_id, provider_id, creator_id, marketplace_date_created, status, server_id, start_time, end_time, server_config, cost):
        self.marketplace_offer_id = marketplace_offer_id
        self.provider_id = provider_id
        self.creator_id = creator_id
        self.marketplace_date_created = marketplace_date_created
        self.status = status
        self.server_id = server_id
        self.start_time = start_time
        self.end_time = end_time
        self.server_config = server_config
        self.cost = cost

    def as_dict(self):
        d = {}
        for col in self.__table__.columns:
            if col.name in ['marketplace_date_created', 'start_time', 'end_time']:
                d[col.name] = getattr(self,  col.name).isoformat()
            else:
                d[col.name] = getattr(self, col.name)
        return d

    @classmethod
    def find_by_id(cls, marketplace_offer_id):
        return cls.query.filter_by(marketplace_offer_id=marketplace_offer_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
