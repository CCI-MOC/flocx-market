from datetime import datetime, timedelta
import unittest.mock as mock

from oslo_context import context as ctx

from flocx_market.common import statuses
from flocx_market.matcher import match_engine
from flocx_market.objects import offer
from flocx_market.objects import bid
from flocx_market.objects import contract
from flocx_market.resource_objects import resource_types

scoped_context = ctx.RequestContext(is_admin=True,
                                    project_id='5599')

now = datetime.utcnow()
test_offer_0 = dict(
    date_created=now,
    status=statuses.AVAILABLE,
    resource_id='4567',
    resource_type=resource_types.IRONIC_NODE,
    start_time=now - timedelta(days=2),
    end_time=now + timedelta(days=2),
    config={'cpu': 4},
    project_id='5599',
    cost=0.0,
    )


test_bid_0 = dict(
    creator_bid_id="12a59a51-b4d6-497d-9f75-f56c409305c8",
    quantity=1,
    start_time=now - timedelta(days=1),
    end_time=now - timedelta(days=1),
    duration=16400,
    status=statuses.AVAILABLE,
    config_query={'foo': 'bar', 'specs': [['cpu', '==', 5]]},
    project_id='5599',
    cost=11.5)

test_bid_1 = dict(
    creator_bid_id="12a59a51-b4d6-497d-9f75",
    quantity=1,
    start_time=now - timedelta(days=1),
    end_time=now - timedelta(days=1),
    duration=16400,
    status=statuses.AVAILABLE,
    config_query={'foo': 'bar', 'specs': [['cpu', '==', 4]]},
    project_id='5599',
    cost=11.5)


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.is_resource_admin')
def test_simple_match(is_resource_admin, app, db, session):
    is_resource_admin.return_vale = True
    offer.Offer.create(test_offer_0, scoped_context)
    bid.Bid.create(test_bid_0, scoped_context)
    match_engine.match(scoped_context)
    assert len(contract.Contract.get_all(scoped_context)) == 0


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.is_resource_admin')
def test_simple_unmatch(is_resource_admin, app, db, session):
    is_resource_admin.return_vale = True
    offer.Offer.create(test_offer_0, scoped_context)
    bid.Bid.create(test_bid_1, scoped_context)
    match_engine.match(scoped_context)
    assert len(contract.Contract.get_all(scoped_context)) == 1


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.is_resource_admin')
def test_time_unmatch(is_resource_admin, app, db, session):
    is_resource_admin.return_vale = True
    test_offer_0['start_time'] = now - timedelta(days=5)
    test_offer_0['end_time'] = now - timedelta(days=4)
    test_bid_1['start_time'] = now - timedelta(days=3)
    test_bid_1['end_time'] = now - timedelta(days=2)
    offer.Offer.create(test_offer_0, scoped_context)
    bid.Bid.create(test_bid_1, scoped_context)
    match_engine.match(scoped_context)
    assert len(contract.Contract.get_all(scoped_context)) == 0


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.is_resource_admin')
def test_one_match(is_resource_admin, app, db, session):
    is_resource_admin.return_vale = True
    test_offer_0['start_time'] = now - timedelta(days=2)
    test_offer_0['end_time'] = now + timedelta(days=2)
    test_bid_1['start_time'] = now - timedelta(days=1)
    test_bid_1['end_time'] = now + timedelta(days=1)
    offer.Offer.create(test_offer_0, scoped_context)
    bid.Bid.create(test_bid_1, scoped_context)
    match_engine.match(scoped_context)
    test_bid_1['creator_bid_id'] = "12a59a51"
    bid.Bid.create(test_bid_1, scoped_context)
    match_engine.match(scoped_context)
    assert len(contract.Contract.get_all(scoped_context)) == 1
