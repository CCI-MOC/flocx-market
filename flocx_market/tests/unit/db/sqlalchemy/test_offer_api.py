import datetime
import pytest

from flocx_market.db.sqlalchemy.offer_api import OfferApi

from sqlalchemy.exc import IntegrityError


now = datetime.datetime.utcnow()
test_offer_data = dict(
    provider_id='2345',
    creator_id='3456',
    marketplace_date_created=now,
    status='available',
    server_id='4567',
    start_time=now,
    end_time=now,
    server_config={'foo': 'bar'},
    cost=0.0,
)


def test_offer_create(app, db, session):
    offer = OfferApi(**test_offer_data)
    offer.save_to_db()
    check = OfferApi.find_by_id(offer.marketplace_offer_id)

    assert check.as_dict() == offer.as_dict()


def test_offer_create_invalid(app, db, session):
    data = dict(test_offer_data)
    del data['provider_id']
    offer = OfferApi(**data)

    with pytest.raises(IntegrityError):
        offer.save_to_db()


def test_offer_delete(app, db, session):
    offer = OfferApi(**test_offer_data)
    offer.save_to_db()
    offer.delete_from_db()
    check = OfferApi.find_by_id(offer.marketplace_offer_id)
    assert check is None
