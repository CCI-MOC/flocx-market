import datetime
import unittest.mock as mock

from oslo_context import context as ctx

from flocx_market.common import statuses
from flocx_market.objects import offer
from flocx_market.resource_objects import resource_types


now = datetime.datetime.utcnow()

test_offer_1 = dict(
    offer_id='1234',
    status=statuses.AVAILABLE,
    resource_id='4567',
    resource_type=resource_types.IRONIC_NODE,
    start_time=now,
    end_time=now,
    config={'foo': 'bar'},
    cost=0.0,
    contract_id=None,
    project_id=5599,
    created_at=now,
    updated_at=now,
)

test_offer_2 = dict(
    offer_id='124',
    status=statuses.AVAILABLE,
    resource_id='456789',
    resource_type=resource_types.IRONIC_NODE,
    start_time=now,
    end_time=now,
    config={'foo': 'bar'},
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
    offer.Offer.get(o.offer_id, scoped_context)
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


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get_all')
def test_related_contracts(ocr_get_all):
    o = offer.Offer(**test_offer_1)
    o.related_contracts(scoped_context)
    ocr_get_all.assert_called_once_with(
        scoped_context,
        {'offer_id': o.offer_id}
    )


@mock.patch('flocx_market.resource_objects.resource_object_factory'
            '.ResourceObjectFactory.get_resource_object')
def test_resource_object(get_resource_object):
    o = offer.Offer(**test_offer_1)
    o.resource_object()
    get_resource_object.assert_called_once_with(o.resource_type, o.resource_id)


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
