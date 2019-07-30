from flocx_market.objects import offer
import datetime
import unittest.mock as mock

from oslo_context import context as ctx


now = datetime.datetime.utcnow()

test_offer_1 = dict(
    marketplace_offer_id='1234',
    provider_offer_id='a41fadc1-6ae9-47e5-a74e-2dcf2b4dd55a',
    status='available',
    server_id='4567',
    start_time=now,
    end_time=now,
    server_config={'foo': 'bar'},
    cost=0.0,
    contract_id=None,
    project_id=5599,
    created_at=now,
    updated_at=now,
)

test_offer_2 = dict(
    marketplace_offer_id='124',
    provider_offer_id='141fadc1-6ae9-47e5-a74e-2dcf2b4dd554',
    status='available',
    server_id='456789',
    start_time=now,
    end_time=now,
    server_config={'foo': 'bar'},
    cost=0.0,
    contract_id=None,
    project_id=5599,
    created_at=now,
    updated_at=now,
)

scoped_context = ctx.RequestContext(is_admin=False,
                                    project_id='5599')


@mock.patch('flocx_market.db.sqlalchemy.api.offer_create')
def test_create(offer_create):
    offer_create.return_value = test_offer_1
    offer.Offer.create(test_offer_1, scoped_context)
    offer_create.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.offer_get')
def test_get(offer_get):
    offer_get.return_value = test_offer_1
    o = offer.Offer(**test_offer_1)
    offer.Offer.get(o.marketplace_offer_id, scoped_context)
    offer_get.assert_called_once()


def test_get_none():
    ret = offer.Offer.get(None, scoped_context)
    assert ret is None


@mock.patch('flocx_market.db.sqlalchemy.api.offer_get_all')
def test_get_all(offer_get_all):
    offer.Offer.get_all(scoped_context)
    offer_get_all.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.offer_get_all_by_project_id')
def test_get_all_by_project_id(offer_get_all):
    offer.Offer.get_all_by_project_id(scoped_context)
    offer_get_all.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.offer_destroy')
def test_destroy(offer_destroy):
    o = offer.Offer(**test_offer_1)
    o.destroy(scoped_context)
    offer_destroy.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.offer_update')
def test_save(offer_update):
    offer_update.return_value = test_offer_1
    o = offer.Offer(**test_offer_1)
    o.status = "busy"
    o.save(scoped_context)
    offer_update.assert_called_once()


@mock.patch('flocx_market.objects.offer.Offer._from_db_object_list')
@mock.patch('flocx_market.objects.offer.db.offer_get_all_unexpired')
def test_update_to_expire(get_all, _from_db_object_list):

    offer.Offer.get_all_unexpired(scoped_context)

    get_all.assert_called_once()


@mock.patch('flocx_market.objects.offer.Offer.save')
def test_expire(save):
    o = offer.Offer(**test_offer_1)
    o.expire(scoped_context)

    save.assert_called_once()
