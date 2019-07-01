import datetime
import json
from unittest import mock

import flocx_market.conf
from flocx_market.db.sqlalchemy import models

CONF = flocx_market.conf.CONF

now = datetime.datetime.utcnow()


test_bid_1 = models.Bid(marketplace_bid_id='test_bid_1',
                        creator_bid_id="1234",
                        creator_id="2345",
                        server_quantity=2,
                        start_time=now,
                        end_time=now,
                        duration=16400,
                        status="available",
                        server_config_query={'foo': 'bar'},
                        cost=11.5)

test_bid_2 = models.Bid(marketplace_bid_id='test_bid_2',
                        creator_bid_id="2345",
                        creator_id="3456",
                        server_quantity=2,
                        start_time=now,
                        end_time=now,
                        duration=16400,
                        status="available",
                        server_config_query={'foo': 'bar'},
                        cost=11.5)


@mock.patch('flocx_market.db.sqlalchemy.api.bid_get_all')
def test_get_bids(mock_get_all, client):
    test_result = [test_bid_1, test_bid_2]
    mock_get_all.return_value = test_result
    response = client.get("/bid", follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 2
    assert any(x['creator_id'] == test_bid_1.creator_id
               for x in response.json)
    assert any(x['creator_id'] == test_bid_2.creator_id
               for x in response.json)


@mock.patch('flocx_market.db.sqlalchemy.api.bid_get')
def test_get_bid(mock_get, client):
    mock_get.return_value = test_bid_1
    response = client.get('/bid/{}'.format(
        test_bid_1.marketplace_bid_id))
    assert response.status_code == 200
    mock_get.assert_called_with('test_bid_1')
    assert response.json['marketplace_bid_id'] == 'test_bid_1'


@mock.patch('flocx_market.db.sqlalchemy.api.bid_get')
def test_get_bid_missing(mock_get, client):
    mock_get.return_value = None
    response = client.get('/bid/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.db.sqlalchemy.api.bid_destroy')
@mock.patch('flocx_market.db.sqlalchemy.api.bid_get')
def test_delete_bid(mock_get, mock_destroy, client):
    mock_get.return_value = test_bid_1
    response = client.delete('/bid/{}'.format(
        test_bid_1.marketplace_bid_id))
    assert response.status_code == 200
    assert mock_destroy.call_count == 1


@mock.patch('flocx_market.db.sqlalchemy.api.bid_get')
def test_delete_bid_missing(mock_get, client):
    mock_get.return_value = None
    response = client.delete('/bid/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.db.sqlalchemy.api.bid_create')
def test_create_bid(mock_create, client):
    mock_create.return_value = test_bid_1
    res = client.post('/bid', data=json.dumps(test_bid_1.to_dict()))
    assert res.status_code == 201
    assert mock_create.call_count == 1
    assert res.json == test_bid_1.to_dict()


@mock.patch('flocx_market.db.sqlalchemy.api.bid_update')
@mock.patch('flocx_market.db.sqlalchemy.api.bid_get')
def test_update_bid(mock_get, mock_update, client):
    mock_get.return_value = test_bid_1
    mock_update.return_value = test_bid_1
    res = client.put('/bid/{}'.format(test_bid_1.marketplace_bid_id),
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 200
    assert mock_update.call_count == 1
    assert res.json['status'] == 'testing'


@mock.patch('flocx_market.db.sqlalchemy.api.bid_update')
@mock.patch('flocx_market.db.sqlalchemy.api.bid_get')
def test_update_bid_missing(mock_get, mock_update,
                            client):
    mock_get.return_value = None
    res = client.put('/bid/does-not-exist',
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 404
    assert mock_update.call_count == 0
