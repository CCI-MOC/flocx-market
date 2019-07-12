from oslo_utils import uuidutils

from flocx_market.db.orm import orm
from flocx_market.db.sqlalchemy.offer_model import OfferModel


def get(marketplace_offer_id):
    return OfferModel.query.filter_by(
        marketplace_offer_id=marketplace_offer_id).first()


def get_all():
    return OfferModel.query.all()


def create(values):
    values['marketplace_offer_id'] = uuidutils.generate_uuid()
    offer_ref = OfferModel(**values)
    orm.session.add(offer_ref)
    orm.session.commit()
    return offer_ref


def update(marketplace_offer_id, values):
    values.pop('marketplace_offer_id', None)
    OfferModel.query.filter_by(
        marketplace_offer_id=marketplace_offer_id).update(values)
    orm.session.commit()
    return get(marketplace_offer_id)


def destroy(marketplace_offer_id):
    offer_ref = get(marketplace_offer_id)
    if offer_ref:
        orm.session.delete(offer_ref)
        orm.session.commit()
