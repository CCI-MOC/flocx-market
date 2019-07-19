from flocx_market.objects import offer
import datetime
import unittest.mock as mock
now = datetime.datetime.utcnow()


test_offer_1 = dict(
    marketplace_offer_id='1234',
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

test_offer_2 = dict(
    marketplace_offer_id='124',
    provider_id='2345',
    creator_id='3456',
    marketplace_date_created=now,
    status='available',
    server_id='456789',
    start_time=now,
    end_time=now,
    server_config={'foo': 'bar'},
    cost=0.0,
)


@mock.patch('flocx_market.db.sqlalchemy.api.offer_create')
def test_create(offer_create):
    offer_create.return_value = test_offer_1
    offer.Offer.create(test_offer_1)
    offer_create.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.offer_get')
def test_get(offer_get):
    offer_get.return_value = test_offer_1
    o = offer.Offer(**test_offer_1)
    offer.Offer.get(o.marketplace_offer_id)
    offer_get.assert_called_once()


def test_get_none():
    ret = offer.Offer.get(None)
    assert ret is None


@mock.patch('flocx_market.db.sqlalchemy.api.offer_get_all')
def test_get_all(offer_get_all):
    offer.Offer.get_all()
    offer_get_all.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.offer_destroy')
def test_destroy(offer_destroy):
    o = offer.Offer(**test_offer_1)
    o.destroy()
    offer_destroy.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.offer_update')
def test_save(offer_update):
    offer_update.return_value = test_offer_1
    o = offer.Offer(**test_offer_1)
    o.status = "busy"
    o.save()
    offer_update.assert_called_once()
