import datetime
import json
from unittest import mock

import flocx_market.conf
from flocx_market.db.sqlalchemy.bid_api import BidApi

CONF = flocx_market.conf.CONF

now = datetime.datetime.utcnow()


test_bid_1 = BidApi(marketplace_bid_id='test_bid_1',
                    creator_bid_id="1234",
                    creator_id="2345",
                    server_quantity=2,
                    start_time=now,
                    end_time=now,
                    duration=16400,
                    status="available",
                    server_config_query={'foo': 'bar'},
                    cost=11.5)

test_bid_2 = BidApi(marketplace_bid_id='test_bid_2',
                    creator_bid_id="2345",
                    creator_id="3456",
                    server_quantity=2,
                    start_time=now,
                    end_time=now,
                    duration=16400,
                    status="available",
                    server_config_query={'foo': 'bar'},
                    cost=11.5)


@mock.patch('flocx_market.api.bid.BidApi.query')
def test_get_bids(mock_query, client):
    test_result = [test_bid_1, test_bid_2]
    mock_query.all.return_value = test_result
    response = client.get("/bid", follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 2
    assert any(x['creator_id'] == test_bid_1.creator_id
               for x in response.json)
    assert any(x['creator_id'] == test_bid_2.creator_id
               for x in response.json)


@mock.patch('flocx_market.api.bid.BidApi.find_by_id')
def test_get_bid(mock_find_by_id, client):
    mock_find_by_id.return_value = test_bid_1
    response = client.get('/bid/{}'.format(
        test_bid_1.marketplace_bid_id))
    assert response.status_code == 200
    mock_find_by_id.assert_called_with('test_bid_1')
    assert response.json['marketplace_bid_id'] == 'test_bid_1'


@mock.patch('flocx_market.api.bid.BidApi.find_by_id')
def test_get_bid_missing(mock_find_by_id, client):
    mock_find_by_id.return_value = None
    response = client.get('/bid/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.api.bid.BidApi.find_by_id')
@mock.patch('flocx_market.api.bid.BidApi.delete_from_db')
def test_delete_bid(mock_delete_from_db, mock_find_by_id, client):
    mock_find_by_id.return_value = test_bid_1
    response = client.delete('/bid/{}'.format(
        test_bid_1.marketplace_bid_id))
    assert response.status_code == 200
    assert mock_delete_from_db.call_count == 1


@mock.patch('flocx_market.api.bid.BidApi.find_by_id')
def test_delete_bid_missing(mock_find_by_id, client):
    mock_find_by_id.return_value = None
    response = client.delete('/bid/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.api.bid.BidApi')
@mock.patch('flocx_market.api.bid.BidApi.save_to_db')
def test_create_bid(mock_save_to_db, mock_bid, client):
    mock_bid.return_value = test_bid_1
    res = client.post('/bid', data=json.dumps(test_bid_1.as_dict()))
    assert res.status_code == 201
    assert mock_save_to_db.call_count == 1
    assert res.json == test_bid_1.as_dict()


@mock.patch('flocx_market.api.bid.BidApi.find_by_id')
@mock.patch('flocx_market.api.bid.BidApi.save_to_db')
def test_update_bid(mock_save_to_db, mock_find_by_id, client):
    mock_find_by_id.return_value = test_bid_1
    res = client.put('/bid/{}'.format(test_bid_1.marketplace_bid_id),
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 200
    assert mock_save_to_db.call_count == 1
    assert res.json['status'] == 'testing'


@mock.patch('flocx_market.api.bid.BidApi.find_by_id')
@mock.patch('flocx_market.api.bid.BidApi.save_to_db')
def test_update_bid_missing(mock_save_to_db, mock_find_by_id,
                            client):
    mock_find_by_id.return_value = None
    res = client.put('/bid/does-not-exist',
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 404
    assert mock_save_to_db.call_count == 0
