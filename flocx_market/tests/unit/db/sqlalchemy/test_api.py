import datetime
import pytest

from oslo_db.exception import DBError

from flocx_market.db.sqlalchemy import api


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

test_offer_data_2 = dict(
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

test_bid_data = dict(creator_bid_id="12a59a51-b4d6-497d-9f75-f56c409305c8",
                     creator_id="12a59a51-b4d6-497d-9f75-f56c409305c8",
                     server_quantity=2,
                     start_time=now,
                     end_time=now,
                     duration=16400,
                     status="available",
                     server_config_query={'foo': 'bar'},
                     cost=11.5)


def test_offer_get_all(app, db, session):
    api.offer_create(test_offer_data)
    api.offer_create(test_offer_data_2)

    assert len(api.offer_get_all()) == 2


def test_offer_create(app, db, session):
    offer = api.offer_create(test_offer_data)
    check = api.offer_get(offer.marketplace_offer_id)

    assert check.to_dict() == offer.to_dict()


def test_offer_create_invalid(app, db, session):
    data = dict(test_offer_data)
    del data['provider_id']

    with pytest.raises(DBError):
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


def test_bid_get_all(app, db, session):
    api.bid_create(test_bid_data)
    api.bid_create(test_bid_data)

    assert len(api.bid_get_all()) == 2


def test_bid_create(app, db, session):
    bid = api.bid_create(test_bid_data)
    check = api.bid_get(bid.marketplace_bid_id)

    assert check.to_dict() == bid.to_dict()


def test_bid_create_invalid(app, db, session):
    data = dict(test_bid_data)
    del data['creator_bid_id']

    with pytest.raises(DBError):
        api.bid_create(data)
    test_bid_data['creator_bid_id'] = '12a59a51-b4d6-497d-9f75-f56c409305c8'


def test_bid_delete(app, db, session):
    bid = api.bid_create(test_bid_data)
    api.bid_destroy(bid.marketplace_bid_id)
    check = api.bid_get(bid.marketplace_bid_id)
    assert check is None


def test_bid_update(app, db, session):
    bid = api.bid_create(test_bid_data)
    bid = api.bid_update(
        bid.marketplace_bid_id, dict(status='testing'))
    check = api.bid_get(bid.marketplace_bid_id)

    assert check.status == 'testing'
    assert check.creator_id == '12a59a51-b4d6-497d-9f75-f56c409305c8'


def create_test_contract_data():
    bid = api.bid_create(test_bid_data)
    offer = api.offer_create(test_offer_data)

    contract_data = dict(
        time_created=now,
        status='available',
        start_time=now,
        end_time=now,
        cost=0.0,
        bid_id=bid.marketplace_bid_id,
        offers=[offer.marketplace_offer_id]
    )
    return contract_data


def test_contract_create(app, db, session):
    contract = api.contract_create(create_test_contract_data())
    check = api.contract_get(contract.contract_id)

    assert check.to_dict() == contract.to_dict()


def test_contract_create_invalid(app, db, session):
    data = create_test_contract_data()
    del data['cost']
    print(data)
    with pytest.raises(DBError):
        api.contract_create(data)


def test_contract_delete(app, db, session):
    contract = api.contract_create(create_test_contract_data())
    api.contract_destroy(contract.contract_id)
    check = api.contract_get(contract.contract_id)
    assert check is None


def test_contract_update(app, db, session):
    contract = api.contract_create(create_test_contract_data())
    contract = api.contract_update(
        contract.contract_id, dict(status='testing'))
    check = api.contract_get(contract.contract_id)

    assert check.status == 'testing'
    assert check.cost == 0.0
