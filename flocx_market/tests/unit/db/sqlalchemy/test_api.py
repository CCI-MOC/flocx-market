import datetime
import pytest

from flocx_market.db.sqlalchemy import api

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
    offer = api.offer_create(test_offer_data)
    check = api.offer_get(offer.marketplace_offer_id)

    assert check.to_dict() == offer.to_dict()


def test_offer_create_invalid(app, db, session):
    data = dict(test_offer_data)
    del data['provider_id']

    with pytest.raises(IntegrityError):
        api.offer_create(data)


def test_offer_delete(app, db, session):
    offer = api.offer_create(test_offer_data)
    api.offer_destroy(offer.marketplace_offer_id)
    check = api.offer_get(offer.marketplace_offer_id)
    assert check is None


def test_offer_update(app, db, session):
    offer = api.offer_create(test_offer_data)
    offer = api.offer_update(
        offer.marketplace_offer_id, dict(status='testing'))
    check = api.offer_get(offer.marketplace_offer_id)

    assert check.status == 'testing'
    assert check.creator_id == '3456'
