from flocx_market.objects import bid
import datetime
import unittest.mock as mock
now = datetime.datetime.utcnow()


test_bid_1 = dict(marketplace_bid_id="123",
                  creator_bid_id="1259a51-b4d6-497d-9f75-f56c409305c8",
                  creator_id="12a59a51",
                  server_quantity=2,
                  start_time=now,
                  end_time=now,
                  duration=16400,
                  status="available",
                  server_config_query={'foo': 'bar'},
                  cost=11.2)

test_bid_2 = dict(marketplace_bid_id="1232",
                  creator_bid_id="12a59a51-b4d6-497d-9f75-f56c409305c8",
                  creator_id="12a9a51",
                  server_quantity=2,
                  start_time=now,
                  end_time=now,
                  duration=16400,
                  status="available",
                  server_config_query={'foo': 'bar'},
                  cost=11.5)


@mock.patch('flocx_market.db.sqlalchemy.api.bid_create')
def test_create(bid_create):
    bid.Bid.create(test_bid_1)
    bid_create.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.bid_get')
def test_get(bid_get):
    b = bid.Bid(**test_bid_2)
    bid.Bid.get(b.marketplace_bid_id)
    bid_get.assert_called_once()


def test_get_none():
    ret = bid.Bid.get(None)
    assert ret is None


@mock.patch('flocx_market.db.sqlalchemy.api.bid_get_all')
def test_get_all(bid_get_all):
    bid.Bid.get_all()
    bid_get_all.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.bid_destroy')
def test_destroy(bid_destroy):
    b = bid.Bid(**test_bid_1)
    b.destroy()
    bid_destroy.assert_called_once()


@mock.patch('flocx_market.db.sqlalchemy.api.bid_update')
def test_save(bid_update):
    b = bid.Bid(**test_bid_1)
    test_bid_1['status'] = "busy"
    b.save(test_bid_1)
    bid_update.assert_called_once()
