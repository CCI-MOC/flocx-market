from datetime import datetime, timedelta
import pytest

from oslo_db.exception import DBError
from oslo_context import context as ctx

from flocx_market.db.sqlalchemy import api

now = datetime.utcnow()

test_offer_data = dict(
    provider_offer_id='a41fadc1-6ae9-47e5-a74e-2dcf2b4dd55a',
    status='available',
    project_id='1234',
    server_id='4567',
    start_time=now - timedelta(days=1),
    end_time=now + timedelta(days=1),
    server_config={'foo': 'bar'},
    cost=0.0,
    )

test_offer_data_2 = dict(
    provider_offer_id='141fadc1-6ae9-47e5-a74e-2dcf2b4dd554',
    status='expired',
    project_id='1234',
    server_id='456789',
    start_time=now - timedelta(days=2),
    end_time=now - timedelta(days=1),
    server_config={'foo': 'bar'},
    cost=0.0,
    )


test_offer_data_3 = dict(
    provider_offer_id='141fadc1-6ae9-47e5-a74e-2dcf2b455555',
    status='available',
    project_id='7788',
    server_id='123',
    start_time=now - timedelta(days=2),
    end_time=now - timedelta(days=1),
    server_config={'foo': 'bar'},
    cost=0.0,
    )

test_bid_data_1 = dict(server_quantity=2,
                       start_time=now - timedelta(days=2),
                       end_time=now - timedelta(days=1),
                       duration=16400,
                       status="available",
                       server_config_query={'foo': 'bar'},
                       cost=11.5)


test_bid_data_2 = dict(server_quantity=2,
                       start_time=now - timedelta(days=2),
                       end_time=now + timedelta(days=1),
                       duration=16400,
                       status="available",
                       server_config_query={'foo': 'bar'},
                       cost=11.5)

test_bid_data_3 = dict(server_quantity=2,
                       start_time=now - timedelta(days=2),
                       end_time=now + timedelta(days=1),
                       duration=16400,
                       status="available",
                       server_config_query={'foo': 'bar'},
                       cost=11.5)

admin_context = ctx.RequestContext(is_admin=True)

scoped_context = ctx.RequestContext(is_admin=False,
                                    project_id='1234')

scoped_context_2 = ctx.RequestContext(is_admin=False,
                                      project_id='7788')


def test_offer_get_all(app, db, session):
    api.offer_create(test_offer_data, scoped_context)
    api.offer_create(test_offer_data_2, scoped_context)
    api.offer_create(test_offer_data_3, scoped_context_2)

    assert len(api.offer_get_all(scoped_context)) == 3


def test_offer_get_all_by_project_id(app, db, session):
    api.offer_create(test_offer_data, scoped_context)
    api.offer_create(test_offer_data_2, scoped_context)
    api.offer_create(test_offer_data_3, scoped_context_2)

    assert len(api.offer_get_all_by_project_id(scoped_context)) == 2


def test_offer_get_all_unexpired_admin(app, db, session):
    api.offer_create(test_offer_data, scoped_context)
    api.offer_create(test_offer_data_2, scoped_context)
    api.offer_create(test_offer_data_3, scoped_context_2)

    offers = api.offer_get_all_unexpired(admin_context)
    assert len(offers) == 2


def test_offer_get_all_unexpired_scoped(app, db, session):
    api.offer_create(test_offer_data, scoped_context)
    api.offer_create(test_offer_data_2, scoped_context)
    api.offer_create(test_offer_data_3, scoped_context_2)

    offers = api.offer_get_all_unexpired(scoped_context)
    assert len(offers) == 1


def test_offer_create(app, db, session):
    offer = api.offer_create(test_offer_data, scoped_context)
    check = api.offer_get(offer.marketplace_offer_id, scoped_context)

    assert check.to_dict() == offer.to_dict()


def test_offer_create_invalid_no_cost_admin(app, db, session):
    data = dict(test_offer_data)
    del data['cost']

    with pytest.raises(DBError):
        api.offer_create(data, scoped_context)


def test_offer_create_invalid_negative_cost_admin(app, db, session):
    data = dict(test_offer_data)
    data['cost'] = -1

    with pytest.raises(ValueError):
        api.offer_create(data, scoped_context)


def test_offer_delete_admin(app, db, session):
    offer = api.offer_create(test_offer_data, scoped_context_2)
    api.offer_destroy(offer.marketplace_offer_id, admin_context)
    check = api.offer_get(offer.marketplace_offer_id, scoped_context_2)
    assert check is None


def test_offer_delete_scoped_valid(app, db, session):
    offer = api.offer_create(test_offer_data, scoped_context)
    api.offer_destroy(offer.marketplace_offer_id, scoped_context)
    check = api.offer_get(offer.marketplace_offer_id, scoped_context)
    assert check is None


def test_offer_delete_scoped_invalid(app, db, session):
    offer = api.offer_create(test_offer_data, scoped_context)
    api.offer_destroy(offer.marketplace_offer_id, scoped_context_2)
    check = api.offer_get(offer.marketplace_offer_id, scoped_context)
    assert check is not None


def test_offer_update_admin(app, db, session):
    offer = api.offer_create(test_offer_data, scoped_context)
    offer = api.offer_update(
        offer.marketplace_offer_id, dict(status='testing'), admin_context)
    check = api.offer_get(offer.marketplace_offer_id, admin_context)

    assert check.status == 'testing'


def test_offer_update_scoped_valid(app, db, session):
    offer = api.offer_create(test_offer_data, scoped_context)
    offer = api.offer_update(
        offer.marketplace_offer_id, dict(status='testing'), scoped_context)
    check = api.offer_get(offer.marketplace_offer_id, scoped_context)

    assert check.status == 'testing'


def test_offer_update_scoped_invalid(app, db, session):
    offer = api.offer_create(test_offer_data, scoped_context)
    update = api.offer_update(
        offer.marketplace_offer_id, dict(status='testing'), scoped_context_2)

    assert update is None

    check = api.offer_get(offer.marketplace_offer_id, scoped_context)
    assert check.status != 'testing'


def test_bid_get(app, db, session):
    api.bid_create(test_bid_data_1, scoped_context)
    api.bid_create(test_bid_data_2, scoped_context)

    assert len(api.bid_get_all(admin_context)) == 2


def test_bid_get_all(app, db, session):
    api.bid_create(test_bid_data_1, scoped_context)
    api.bid_create(test_bid_data_2, scoped_context)

    assert len(api.bid_get_all(admin_context)) == 2


def test_bid_get_all_by_project_id(app, db, session):
    api.bid_create(test_bid_data_1, scoped_context)
    api.bid_create(test_bid_data_2, scoped_context)

    assert len(api.bid_get_all(admin_context)) == 2


def test_bid_get_all_unexpired(app, db, session):
    api.bid_create(test_bid_data_1, scoped_context)
    api.bid_create(test_bid_data_2, scoped_context)

    bids = api.bid_get_all(scoped_context)

    assert len(api.bid_get_all(scoped_context)) == 2
    assert len(api.bid_get_all_unexpired(scoped_context)) == 2

    api.bid_update(
        bids[1].marketplace_bid_id, dict(status='expired'), scoped_context)
    assert len(api.bid_get_all_unexpired(scoped_context)) == 1


def test_bid_create(app, db, session):
    bid = api.bid_create(test_bid_data_1, scoped_context)
    check = api.bid_get(bid.marketplace_bid_id, scoped_context)

    assert check.to_dict() == bid.to_dict()


def test_bid_create_invalid(app, db, session):
    data = dict(test_bid_data_1)
    del data['cost']

    with pytest.raises(DBError):
        api.bid_create(data, scoped_context)
    test_bid_data_1['creator_bid_id'] = '12a59a51-b4d6-497d-9f75-f56c409305c8'


def test_bid_delete_admin(app, db, session):
    bid = api.bid_create(test_bid_data_1, scoped_context)
    api.bid_destroy(bid.marketplace_bid_id, admin_context)
    check = api.bid_get(bid.marketplace_bid_id, scoped_context)
    assert check is None


def test_bid_delete_scoped_valid(app, db, session):
    bid = api.bid_create(test_bid_data_1, scoped_context)
    api.bid_destroy(bid.marketplace_bid_id, scoped_context)
    check = api.bid_get(bid.marketplace_bid_id, scoped_context)
    assert check is None


def test_bid_delete_scoped_invalid(app, db, session):
    bid = api.bid_create(test_bid_data_1, scoped_context)
    api.bid_destroy(bid.marketplace_bid_id, scoped_context_2)
    check = api.bid_get(bid.marketplace_bid_id, scoped_context)
    assert check is not None


def test_bid_update_admin(app, db, session):
    bid = api.bid_create(test_bid_data_1, scoped_context)
    bid = api.bid_update(
        bid.marketplace_bid_id, dict(status='testing'), admin_context)
    check = api.bid_get(bid.marketplace_bid_id, scoped_context)

    assert check.status == 'testing'


def test_bid_update_scoped_valid(app, db, session):
    bid = api.bid_create(test_bid_data_1, scoped_context)
    bid = api.bid_update(
        bid.marketplace_bid_id, dict(status='testing'), scoped_context)
    check = api.bid_get(bid.marketplace_bid_id, scoped_context)

    assert check.status == 'testing'


def test_bid_update_scoped_invalid(app, db, session):
    bid = api.bid_create(test_bid_data_1, scoped_context)
    updated = api.bid_update(bid.marketplace_bid_id,
                             dict(status='testing'),
                             scoped_context_2)

    assert updated is None


def create_test_contract_data():
    bid = api.bid_create(test_bid_data_1, scoped_context)
    offer = api.offer_create(test_offer_data, scoped_context)

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
    api.contract_create(contract_data, admin_context)

    assert len(api.contract_get_all(scoped_context)) == 1


def test_contract_create_valid_admin(app, db, session):
    contract = api.contract_create(create_test_contract_data(), admin_context)
    check = api.contract_get(contract.contract_id, admin_context)

    assert check.to_dict() == contract.to_dict()


def test_contract_create_invalid_admin(app, db, session):
    data = create_test_contract_data()
    del data['cost']
    with pytest.raises(DBError):
        api.contract_create(data, admin_context)


def test_contract_create_invalid_scoped(app, db, session):
    data = create_test_contract_data()
    created = api.contract_create(data, scoped_context)
    assert created is None


def test_contract_delete_valid_admin(app, db, session):
    contract = api.contract_create(create_test_contract_data(), admin_context)
    api.contract_destroy(contract.contract_id, admin_context)
    check = api.contract_get(contract.contract_id, admin_context)
    assert check is None


def test_contract_delete_invalid_scoped(app, db, session):
    contract = api.contract_create(create_test_contract_data(), admin_context)
    destroyed = api.contract_destroy(contract.contract_id, scoped_context)
    check = api.contract_get(contract.contract_id, admin_context)
    assert check is not None
    assert destroyed is None


def test_contract_update_valid_admin(app, db, session):
    contract = api.contract_create(create_test_contract_data(), admin_context)
    contract = api.contract_update(
        contract.contract_id, dict(status='testing'), admin_context)
    check = api.contract_get(contract.contract_id, admin_context)

    assert check.status == 'testing'
    assert check.cost == 0.0


def test_contract_update_invalid_scoped(app, db, session):
    contract = api.contract_create(create_test_contract_data(), admin_context)
    updated = api.contract_update(
        contract.contract_id, dict(status='testing'), scoped_context)
    check = api.contract_get(contract.contract_id, admin_context)

    assert check.status != 'testing'
    assert check.cost == 0.0
    assert updated is None


def test_contract_get_all_unexpired(app, db, session):
    contract = api.contract_create(create_test_contract_data(), admin_context)

    assert len(api.contract_get_all_unexpired(admin_context)) == 1

    api.contract_update(contract.contract_id, dict(status='expired'),
                        admin_context)
    assert len(api.contract_get_all_unexpired(admin_context)) == 0


def create_test_contract_data_for_ocr():
    bid = api.bid_create(test_bid_data_1, scoped_context)
    offer = api.offer_create(test_offer_data, scoped_context)

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
    api.contract_create(contract_data, admin_context)

    assert len(api.offer_contract_relationship_get_all(admin_context)) == 1


def test_offer_contract_relationship_get_by_id(app, db, session):
    contract_data, _ = create_test_contract_data_for_ocr()
    api.contract_create(contract_data, admin_context)
    ocr = api.offer_contract_relationship_get_all(admin_context)
    assert len(api.offer_contract_relationship_get_all(admin_context)) == 1
    assert (api.offer_contract_relationship_get(
        context=admin_context,
        offer_contract_relationship_id=ocr[0].offer_contract_relationship_id)
            .offer_contract_relationship_id ==
            ocr[0].offer_contract_relationship_id)


def test_offer_contract_relationship_create_valid(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data, admin_context)
    filters = {
        'marketplace_offer_id': offer_test_id,
        'contract_id': contract.contract_id
    }
    ocr = api.offer_contract_relationship_get_all(
        context=admin_context,
        filters=filters,
    )
    assert contract.contract_id == ocr[0].contract_id


def test_offer_contract_relationship_create_invalid_scoped(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data, scoped_context)

    assert contract is None


def test_offer_contract_relationship_delete_valid(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data, admin_context)
    filters = {
        'marketplace_offer_id': offer_test_id,
        'contract_id': contract.contract_id
    }
    ocrs = api.offer_contract_relationship_get_all(
        context=admin_context,
        filters=filters,
    )
    ocr_id = ocrs[0].offer_contract_relationship_id
    api.offer_contract_relationship_destroy(
        context=admin_context,
        offer_contract_relationship_id=ocr_id)
    check = api.offer_contract_relationship_get(
        admin_context,
        ocr_id)
    assert check is None


def test_offer_contract_relationship_delete_invalid_scoped(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data, admin_context)
    filters = {
        'marketplace_offer_id': offer_test_id,
        'contract_id': contract.contract_id
    }
    ocrs = api.offer_contract_relationship_get_all(
        context=admin_context,
        filters=filters,
    )
    ocr_id = ocrs[0].offer_contract_relationship_id
    api.offer_contract_relationship_destroy(
        context=scoped_context,
        offer_contract_relationship_id=ocr_id)
    check = api.offer_contract_relationship_get(
        admin_context,
        ocr_id)
    assert check is not None


def test_offer_contract_relationship_update_valid(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data, admin_context)
    filters = {
        'marketplace_offer_id': offer_test_id,
        'contract_id': contract.contract_id
    }
    ocrs = api.offer_contract_relationship_get_all(
        context=admin_context,
        filters=filters,
    )
    ocr_id = ocrs[0].offer_contract_relationship_id

    api.offer_contract_relationship_update(
        context=admin_context,
        offer_contract_relationship_id=ocr_id,
        values=dict(status='testing'))
    check = api.offer_contract_relationship_get(
        context=admin_context,
        offer_contract_relationship_id=ocr_id)

    assert check.status == 'testing'
    assert check.marketplace_offer_id == offer_test_id


# TODO(tzumainn): refactor once we re-enable ocr scoping for the update operation
# def test_offer_contract_relationship_update_invalid_scoped(app, db, session):
#     contract_data, offer_test_id = create_test_contract_data_for_ocr()
#     contract = api.contract_create(contract_data, admin_context)
#     filters = {
#         'marketplace_offer_id': offer_test_id,
#         'contract_id': contract.contract_id
#     }
#     ocrs = api.offer_contract_relationship_get_all(
#         context=admin_context,
#         filters=filters,
#     )
#     ocr_id = ocrs[0].offer_contract_relationship_id

#     api.offer_contract_relationship_update(
#         context=scoped_context,
#         offer_contract_relationship_id=ocr_id,
#         values=dict(status='testing'))
#     check = api.offer_contract_relationship_get(
#         context=admin_context,
#         offer_contract_relationship_id=ocr_id)

#     assert check.status != 'testing'
#     assert check.marketplace_offer_id == offer_test_id


def test_offer_contract_relationship_get_all_unexpired(app, db, session):
    contract_data, offer_test_id = create_test_contract_data_for_ocr()
    contract = api.contract_create(contract_data, admin_context)
    filters = {
        'marketplace_offer_id': offer_test_id,
        'contract_id': contract.contract_id
    }
    ocrs = api.offer_contract_relationship_get_all(
        context=admin_context,
        filters=filters,
    )
    ocr_id = ocrs[0].offer_contract_relationship_id

    assert len(api.offer_contract_relationship_get_all_unexpired(
        admin_context)) == 1

    api.offer_contract_relationship_update(
        context=admin_context,
        offer_contract_relationship_id=ocr_id,
        values=dict(status='expired'))
    assert len(api.offer_contract_relationship_get_all_unexpired(
        admin_context)) == 0
