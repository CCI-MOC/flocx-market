from datetime import datetime, timedelta
import unittest.mock as mock

from oslo_context import context as ctx

from flocx_market.common import statuses
from flocx_market.objects import contract
from flocx_market.objects import offer_contract_relationship as ocr

now = datetime.utcnow()


test_contract_dict_1 = dict(contract_id='1234',
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

test_contract_dict = dict(contract_id='test_contract_2',
                          time_created="2016-07-16T19:20:30",
                          status=statuses.AVAILABLE,
                          start_time=now,
                          end_time=now,
                          cost=0.0,
                          bid_id='test_bid_2',
                          bid=None,
                          offers=['test_offer_1'],
                          project_id='5599',
                          created_at=now,
                          updated_at=now,
                          )

test_ocr_dict = dict(
    offer_contract_relationship_id='test_offer_contract_relationship_id',
    contract_id='1234',
    offer_id='5678',
    status=statuses.AVAILABLE,
    created_at=now,
    updated_at=now,
)

scoped_context = ctx.RequestContext(is_admin=False,
                                    project_id='5599')


@mock.patch('flocx_market.db.sqlalchemy.api.contract_create')
def test_create(contract_create):
    contract_create.return_value = test_contract_dict
    contract.Contract.create(test_contract_dict, scoped_context)
    contract_create.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.contract_get')
def test_get(contract_get):
    contract_get.return_value = test_contract_dict
    c = contract.Contract(**test_contract_dict)
    contract.Contract.get(c.contract_id, scoped_context)
    contract_get.assert_called_once()


def test_get_none():
    ret = contract.Contract.get(None, scoped_context)
    assert ret is None


@mock.patch('flocx_market.db.sqlalchemy.api.contract_get_all')
def test_get_all(contract_get_all):
    contract.Contract.get_all(scoped_context)
    contract_get_all.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.contract_get_all_by_status')
def test_get_all_by_status(contract_get_all_by_status):
    contract.Contract.get_all_by_status(scoped_context, statuses.AVAILABLE)
    contract_get_all_by_status.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.contract_destroy')
def test_destroy(contract_destroy):
    c = contract.Contract(**test_contract_dict)
    c.destroy(scoped_context)
    contract_destroy.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.contract_update')
def test_save(contract_update):
    contract_update.return_value = test_contract_dict
    c = contract.Contract(**test_contract_dict)
    c.status = statuses.EXPIRED
    c.save(scoped_context)
    contract_update.assert_called_once()


@mock.patch('flocx_market.objects.contract.Contract._from_db_object_list')
@mock.patch('flocx_market.objects.contract.db.contract_get_all_unexpired')
def test_update_to_expire(get_all, _from_db_object_list):
    contract.Contract.get_all_unexpired(scoped_context)

    get_all.assert_called_once()


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.fulfill')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get_all')
@mock.patch('flocx_market.objects.contract.Contract.save')
def test_fulfill(save, ocr_get_all, ocr_fulfill):
    ocr_get_all.return_value = [ocr.OfferContractRelationship(**test_ocr_dict)]

    c = contract.Contract(**test_contract_dict_1)
    c.fulfill(scoped_context)

    ocr_fulfill.assert_called_once()
    save.assert_called_once()


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.expire')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get_all')
@mock.patch('flocx_market.objects.contract.Contract.save')
def test_expire(save, ocr_get_all, ocr_expire):
    ocr_get_all.return_value = [ocr.OfferContractRelationship(**test_ocr_dict)]

    c = contract.Contract(**test_contract_dict_1)
    c.expire(scoped_context)

    ocr_expire.assert_called_once()
    save.assert_called_once()
