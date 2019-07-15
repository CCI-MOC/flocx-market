from oslo_db.sqlalchemy import session as db_session
from oslo_utils import uuidutils

import flocx_market.conf
from flocx_market.db.sqlalchemy import models


CONF = flocx_market.conf.CONF
_engine_facade = None


def get_facade():
    global _engine_facade
    if not _engine_facade:
        _engine_facade = db_session.EngineFacade.from_config(CONF)

    return _engine_facade


def get_session():
    return get_facade().get_session()


def reset_facade():
    global _engine_facade
    _engine_facade = None


def setup_db():
    engine = get_facade().get_engine()
    models.Base.metadata.create_all(engine)
    return True


def drop_db():
    engine = db_session.EngineFacade(CONF.database.connection,
                                     sqlite_fk=True).get_engine()
    models.Base.metadata.drop_all(engine)
    return True


def offer_get(marketplace_offer_id):
    return get_session().query(models.Offer).filter_by(
        marketplace_offer_id=marketplace_offer_id).first()


def offer_get_all():
    return get_session().query(models.Offer).all()


def offer_create(values):
    values['marketplace_offer_id'] = uuidutils.generate_uuid()
    offer_ref = models.Offer()
    offer_ref.update(values)
    offer_ref.save(get_session())
    return offer_ref


def offer_update(marketplace_offer_id, values):
    offer_ref = offer_get(marketplace_offer_id)
    values.pop('marketplace_offer_id', None)
    offer_ref.update(values)
    offer_ref.save(get_session())
    return offer_ref


def offer_destroy(marketplace_offer_id):
    offer_ref = offer_get(marketplace_offer_id)
    if offer_ref:
        get_session().query(models.Offer).filter_by(
            marketplace_offer_id=marketplace_offer_id).delete()


def bid_get(marketplace_bid_id):
    return get_session().query(models.Bid).filter_by(
        marketplace_bid_id=marketplace_bid_id).first()


def bid_get_all():
    return get_session().query(models.Bid).all()


def bid_create(values):
    values['marketplace_bid_id'] = uuidutils.generate_uuid()
    bid_ref = models.Bid()
    bid_ref.update(values)
    bid_ref.save(get_session())
    return bid_ref


def bid_update(marketplace_bid_id, values):
    bid_ref = bid_get(marketplace_bid_id)
    values.pop('marketplace_bid_id', None)
    bid_ref.update(values)
    bid_ref.save(get_session())
    return bid_ref


def bid_destroy(marketplace_bid_id):
    bid_ref = bid_get(marketplace_bid_id)
    if bid_ref:
        get_session().query(models.Bid).filter_by(
            marketplace_bid_id=marketplace_bid_id).delete()
