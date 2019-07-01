from oslo_utils import uuidutils

from flocx_market.db.orm import orm
from flocx_market.db.sqlalchemy import models


def offer_get(marketplace_offer_id):
    return models.Offer.query.filter_by(
        marketplace_offer_id=marketplace_offer_id).first()


def offer_get_all():
    return models.Offer.query.all()


def offer_create(**values):
    values['marketplace_offer_id'] = uuidutils.generate_uuid()
    offer_ref = models.Offer(**values)
    orm.session.add(offer_ref)
    orm.session.commit()
    return offer_ref


def offer_update(marketplace_offer_id, values):
    values.pop('marketplace_offer_id', None)
    models.Offer.query.filter_by(
        marketplace_offer_id=marketplace_offer_id).update(values)
    orm.session.commit()
    return offer_get(marketplace_offer_id)


def offer_destroy(marketplace_offer_id):
    offer_ref = offer_get(marketplace_offer_id)
    if offer_ref:
        orm.session.delete(offer_ref)
        orm.session.commit()


def bid_get(marketplace_bid_id):
    return models.Bid.query.filter_by(
        marketplace_bid_id=marketplace_bid_id).first()


def bid_get_all():
    return models.Bid.query.all()


def bid_create(**values):
    values['marketplace_bid_id'] = uuidutils.generate_uuid()
    bid_ref = models.Bid(**values)
    orm.session.add(bid_ref)
    orm.session.commit()
    return bid_ref


def bid_update(marketplace_bid_id, values):
    values.pop('marketplace_bid_id', None)
    models.Bid.query.filter_by(
        marketplace_bid_id=marketplace_bid_id).update(values)
    orm.session.commit()
    return bid_get(marketplace_bid_id)


def bid_destroy(marketplace_bid_id):
    bid_ref = bid_get(marketplace_bid_id)
    if bid_ref:
        orm.session.delete(bid_ref)
        orm.session.commit()
