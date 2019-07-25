from flocx_market.objects import contract
from datetime import datetime, timedelta
import unittest.mock as mock
from oslo_context import context as ctx

now = datetime.utcnow()


test_contract_dict_1 = dict(contract_id='test_contract_2',
                            time_created="2016-07-16T19:20:30",
                            status='available',
                            start_time=now - timedelta(days=2),
                            end_time=now - timedelta(days=1),
                            cost=0.0,
                            bid_id='test_bid_2',
                            bid=None,
                            offers=['test_offer_1']
                            )

test_contract_dict = dict(contract_id='test_contract_2',
                          time_created="2016-07-16T19:20:30",
                          status='available',
                          start_time=now,
                          end_time=now,
                          cost=0.0,
                          bid_id='test_bid_2',
                          bid=None,
                          offers=['test_offer_1'],
                          project_id='5599'
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


@mock.patch('flocx_market.db.sqlalchemy.api.contract_destroy')
def test_destroy(contract_destroy):
    c = contract.Contract(**test_contract_dict)
    c.destroy(scoped_context)
    contract_destroy.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.contract_update')
def test_save(contract_update):
    contract_update.return_value = test_contract_dict
    c = contract.Contract(**test_contract_dict)
    c.status = "busy"
    c.save(scoped_context)
    contract_update.assert_called_once()


@mock.patch('flocx_market.objects.contract.Contract._from_db_object_list')
@mock.patch('flocx_market.objects.contract.db.contract_get_all_unexpired')
def test_update_to_expire(get_all, _from_db_object_list):

    contract.Contract.get_all_unexpired(scoped_context)

    get_all.assert_called_once()


@mock.patch('flocx_market.objects.contract.Contract.save')
def test_expire(save):
    o = contract.Contract(**test_contract_dict_1)
    o.expire(scoped_context)

    save.assert_called_once()
