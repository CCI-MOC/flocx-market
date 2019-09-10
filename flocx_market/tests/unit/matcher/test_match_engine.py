from flocx_market.matcher import match_engine
from flocx_market.objects import offer
from flocx_market.objects import bid
from flocx_market.objects import contract
from datetime import datetime, timedelta
from oslo_context import context as ctx

scoped_context = ctx.RequestContext(is_admin=True,
                                    project_id='5599')

now = datetime.utcnow()
test_offer_0 = dict(
    provider_offer_id='a41fadc1-6ae9-47e5-a74e-2dcf2b4dd55a',
    provider_id='2345',
    marketplace_date_created=now,
    status='available',
    resource_id='4567',
    resource_type='ironic_node',
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
    status="available",
    config_query={'foo': 'bar', 'specs': [['cpu', '==', 5]]},
    project_id='5599',
    cost=11.5)

test_bid_1 = dict(
    creator_bid_id="12a59a51-b4d6-497d-9f75",
    quantity=1,
    start_time=now - timedelta(days=1),
    end_time=now - timedelta(days=1),
    duration=16400,
    status="available",
    config_query={'foo': 'bar', 'specs': [['cpu', '==', 4]]},
    project_id='5599',
    cost=11.5)


def test_simple_match(app, db, session):
    offer.Offer.create(test_offer_0, scoped_context)
    bid.Bid.create(test_bid_0, scoped_context)
    match_engine.match(scoped_context)
    assert len(contract.Contract.get_all(scoped_context)) == 0


def test_simple_unmatch(app, db, session):
    offer.Offer.create(test_offer_0, scoped_context)
    bid.Bid.create(test_bid_1, scoped_context)
    match_engine.match(scoped_context)
    assert len(contract.Contract.get_all(scoped_context)) == 1


def test_time_unmatch(app, db, session):
    test_offer_0['start_time'] = now - timedelta(days=5)
    test_offer_0['end_time'] = now - timedelta(days=4)
    test_bid_1['start_time'] = now - timedelta(days=3)
    test_bid_1['end_time'] = now - timedelta(days=2)
    offer.Offer.create(test_offer_0, scoped_context)
    bid.Bid.create(test_bid_1, scoped_context)
    match_engine.match(scoped_context)
    assert len(contract.Contract.get_all(scoped_context)) == 0


def test_one_match(app, db, session):
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
