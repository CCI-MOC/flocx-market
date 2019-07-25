from datetime import datetime, timedelta
import pytest

from oslo_db.exception import DBError

from flocx_market.db.sqlalchemy import api


now = datetime.utcnow()

test_offer_data = dict(
    provider_offer_id='a41fadc1-6ae9-47e5-a74e-2dcf2b4dd55a',
    provider_id='2345',
    marketplace_date_created=now,
    status='available',
    server_id='4567',
    start_time=now - timedelta(days=1),
    end_time=now + timedelta(days=1),
    server_config={'foo': 'bar'},
    cost=0.0,
    project_id='5599')

test_offer_data_2 = dict(
    provider_offer_id='141fadc1-6ae9-47e5-a74e-2dcf2b4dd554',
    provider_id='2345',
    marketplace_date_created=now,
    status='available',
    server_id='456789',
    start_time=now - timedelta(days=2),
    end_time=now - timedelta(days=1),
    server_config={'foo': 'bar'},
    cost=0.0,
    project_id='5599')


test_bid_data_1 = dict(creator_bid_id="12a59a51-b4d6-497d-9f75-f56c409305c8",
                       server_quantity=2,
                       start_time=now - timedelta(days=2),
                       end_time=now - timedelta(days=1),
                       duration=16400,
                       status="available",
                       server_config_query={'foo': 'bar'},
                       project_id='5599',
                       cost=11.5)


test_bid_data_2 = dict(creator_bid_id="12a59a51-b4d6-497d-9f75-f56c409305c8",
                       server_quantity=2,
                       start_time=now - timedelta(days=2),
                       end_time=now + timedelta(days=1),
                       duration=16400,
                       status="available",
                       server_config_query={'foo': 'bar'},
                       project_id='5599',
                       cost=11.5)


def test_offer_get_all(app, db, session):
    api.offer_create(test_offer_data)
    api.offer_create(test_offer_data_2)

    assert len(api.offer_get_all()) == 2


def test_offer_get_all_to_be_expired(app, db, session):
    api.offer_create(test_offer_data)
    api.offer_create(test_offer_data_2)

    offers = api.offer_get_all()
    assert(offers[0].end_time > now)
    assert(offers[1].end_time < now)

    assert len(api.offer_get_all()) == 2
    assert len(api.offer_get_all_unexpired()) == 2

    api.offer_update(offers[1].marketplace_offer_id, dict(status='expired'))
    assert len(api.offer_get_all_unexpired()) == 1


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


def test_bid_get_all(app, db, session):
    api.bid_create(test_bid_data_1)
    api.bid_create(test_bid_data_2)

    assert len(api.bid_get_all()) == 2


def test_bid_get_all_to_be_expired(app, db, session):
    api.bid_create(test_bid_data_1)
    api.bid_create(test_bid_data_2)

    bids = api.bid_get_all()

    assert len(api.bid_get_all()) == 2
    assert len(api.bid_get_all_unexpired()) == 2

    api.bid_update(bids[1].marketplace_bid_id, dict(status='expired'))
    assert len(api.bid_get_all_unexpired()) == 1


def test_bid_create(app, db, session):
    bid = api.bid_create(test_bid_data_1)
    check = api.bid_get(bid.marketplace_bid_id)

    assert check.to_dict() == bid.to_dict()


def test_bid_create_invalid(app, db, session):
    data = dict(test_bid_data_1)
    del data['creator_bid_id']

    with pytest.raises(DBError):
        api.bid_create(data)
    test_bid_data_1['creator_bid_id'] = '12a59a51-b4d6-497d-9f75-f56c409305c8'


def test_bid_delete(app, db, session):
    bid = api.bid_create(test_bid_data_1)
    api.bid_destroy(bid.marketplace_bid_id)
    check = api.bid_get(bid.marketplace_bid_id)
    assert check is None


def test_bid_update(app, db, session):
    bid = api.bid_create(test_bid_data_1)
    bid = api.bid_update(
        bid.marketplace_bid_id, dict(status='testing'))
    check = api.bid_get(bid.marketplace_bid_id)

    assert check.status == 'testing'


def create_test_contract_data():
    bid = api.bid_create(test_bid_data_1)
    offer = api.offer_create(test_offer_data)

    contract_data = dict(
        time_created=now,
        status='available',
        start_time=now - timedelta(days=2),
        end_time=now - timedelta(days=1),
        cost=0.0,
        bid_id=bid.marketplace_bid_id,
        offers=[offer.marketplace_offer_id],
        project_id='5599'
    )

    return contract_data


def test_contract_get_all(app, db, session):
    contract_data = create_test_contract_data()
    api.contract_create(contract_data)

    assert len(api.contract_get_all()) == 1


def test_contract_create(app, db, session):
    contract = api.contract_create(create_test_contract_data())
    check = api.contract_get(contract.contract_id)

    assert check.to_dict() == contract.to_dict()


def test_contract_create_invalid(app, db, session):
    data = create_test_contract_data()
    del data['cost']
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


def test_contract_get_all_to_be_expired(app, db, session):
    contract = api.contract_create(create_test_contract_data())

    assert len(api.contract_get_all_unexpired()) == 1

    api.contract_update(contract.contract_id, dict(status='expired'))
    assert len(api.contract_get_all_unexpired()) == 0


def create_test_contract_data_for_ocr():
    bid = api.bid_create(test_bid_data_1)
    offer = api.offer_create(test_offer_data)

    contract_data = dict(
        time_created=now,
        status='available',
        start_time=now - timedelta(days=2),
        end_time=now - timedelta(days=1),
        cost=0.0,
        bid_id=bid.marketplace_bid_id,
        offers=[offer.marketplace_offer_id],
        project_id='5599'
    )

    return contract_data, offer.marketplace_offer_id


# contract_offer_relationship
def test_offer_contract_relationship_get_all(app, db, session):
    contract_data, _ = create_test_contract_data_for_ocr()
    api.contract_create(contract_data)

    assert len(api.offer_contract_relationship_get_all()) == 1


def test_offer_contract_relationship_create(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data)
    ocr = api.offer_contract_relationship_get(offer_test_id,
                                              contract.contract_id)
    assert contract.contract_id == ocr.contract_id


def test_offer_contract_relationship_delete(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data)
    api.offer_contract_relationship_destroy(contract.contract_id,
                                            offer_test_id)
    check = api.offer_contract_relationship_get(contract.contract_id,
                                                offer_test_id)
    assert check is None


def test_offer_contract_relationship_update(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data)
    ocr = api.offer_contract_relationship_get(offer_test_id,
                                              contract.contract_id)
    api.offer_contract_relationship_update(
        ocr.marketplace_offer_id,
        ocr.contract_id,
        dict(status='testing'))
    check = api.offer_contract_relationship_get(offer_test_id,
                                                contract.contract_id)

    assert check.status == 'testing'
    assert check.marketplace_offer_id == offer_test_id


def test_offer_contract_relationship_get_all_to_be_expired(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data)
    api.offer_contract_relationship_get(offer_test_id, contract.contract_id)

    assert len(api.offer_contract_relationship_get_all_unexpired()) == 1

    api.offer_contract_relationship_update(offer_test_id, contract.contract_id,
                                           dict(status='expired'))
    assert len(api.offer_contract_relationship_get_all_unexpired()) == 0
