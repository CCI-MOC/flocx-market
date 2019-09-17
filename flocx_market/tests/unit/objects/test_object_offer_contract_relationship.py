from datetime import datetime, timedelta
import pytest
import unittest.mock as mock

from oslo_context import context as ctx

from flocx_market.common import exception as e
from flocx_market.common import statuses
from flocx_market.objects import contract as contract_obj
from flocx_market.objects import offer as offer_obj
from flocx_market.objects import offer_contract_relationship as ocr
from flocx_market.resource_objects import resource_types


now = datetime.utcnow()

test_ocr_dict = dict(
    offer_contract_relationship_id='test_offer_contract_relationship_id',
    contract_id='5678',
    offer_id='1234',
    status=statuses.AVAILABLE,
    created_at=now,
    updated_at=now,
)

test_offer_dict = dict(
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

test_contract_dict = dict(
    contract_id='5678',
    time_created="2016-07-16T19:20:30",
    status=statuses.AVAILABLE,
    start_time=now - timedelta(days=2),
    end_time=now - timedelta(days=1),
    cost=0.0,
    bid_id='test_bid_2',
    bid=None,
    offers=['test_offer_1'],
    created_at=now,
    updated_at=now,
)

scoped_context = ctx.RequestContext(is_admin=False,
                                    project_id='5599')


@mock.patch('flocx_market.db.sqlalchemy.api.offer_contract_relationship_get')
def test_get_by_id(offer_contract_relationship_get):
    offer_contract_relationship_get.return_value = test_ocr_dict
    ocr.OfferContractRelationship(**test_ocr_dict)
    ocr.OfferContractRelationship.get(scoped_context,
                                      'test_offer_contract_relationship_id')
    offer_contract_relationship_get.assert_called_once()


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_get_all')
def test_get_all_with_vals(offer_contract_relationship_get_all):
    offer_contract_relationship_get_all.return_value = [test_ocr_dict]
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    filters = {
        'offer_id': oc.offer_id,
        'contract_id': oc.contract_id,
        'status': oc.status
    }
    ocr.OfferContractRelationship.get_all(scoped_context, filters)
    offer_contract_relationship_get_all.assert_called_once()


def test_get_invalid():
    with pytest.raises(e.ResourceNotFound) as excinfo:
        ocr.OfferContractRelationship.get(scoped_context, 'does-not-exist')
    assert (excinfo.value.code == 404)


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_get_all')
def test_get_all(offer_contract_relationship_get_all):
    ocr.OfferContractRelationship.get_all(scoped_context)
    offer_contract_relationship_get_all.assert_called_once()


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_destroy')
def test_destroy(offer_contract_relationship_destroy):
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.destroy(scoped_context)
    offer_contract_relationship_destroy.assert_called_once()


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_update')
def test_save(offer_contract_relationship_update):
    offer_contract_relationship_update.return_value = test_ocr_dict
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.status = statuses.FULFILLED
    oc.save(scoped_context)
    offer_contract_relationship_update.assert_called_once()


@mock.patch(
    'flocx_market.objects.offer.Offer.get')
def test_offer(get):
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.offer(scoped_context)
    get.assert_called_once_with(oc.offer_id, scoped_context)


@mock.patch(
    'flocx_market.objects.contract.Contract.get')
def test_contract(get):
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.contract(scoped_context)
    get.assert_called_once_with(oc.contract_id, scoped_context)


@mock.patch(
    'flocx_market.objects.offer_contract_relationship'
    '.OfferContractRelationship._from_db_object_list')
@mock.patch(
    'flocx_market.objects.offer_contract_relationship.db'
    '.offer_contract_relationship_get_all_unexpired')
def test_update_to_expire(get_all, _from_db_object_list):
    ocr.OfferContractRelationship.get_all_unexpired(scoped_context)
    get_all.assert_called_once()


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.set_contract')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.contract')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.offer')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.save')
def test_fulfill(save, offer, contract, set_contract):
    offer.return_value = offer_obj.Offer(**test_offer_dict)
    contract.return_value = contract_obj.Contract(**test_contract_dict)

    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.fulfill(scoped_context)

    save.assert_called_once()


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.get_contract_uuid')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.contract')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.offer')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.save')
def test_expire(save, offer, contract, get_contract_uuid):
    offer.return_value = offer_obj.Offer(**test_offer_dict)
    contract.return_value = contract_obj.Contract(**test_contract_dict)
    get_contract_uuid.return_value = None

    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.expire(scoped_context)

    save.assert_called_once()
