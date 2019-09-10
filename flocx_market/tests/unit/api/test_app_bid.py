import datetime
import json
from unittest import mock
from oslo_context import context as ctx

import flocx_market.conf
from flocx_market.objects import bid
from flocx_market.common import exception as e

CONF = flocx_market.conf.CONF

now = datetime.datetime.utcnow()


test_bid_1 = bid.Bid(
    marketplace_bid_id='test_bid_1',
    creator_bid_id="1234",
    quantity=2,
    start_time=now,
    end_time=now,
    duration=16400,
    status="available",
    config_query={'foo': 'bar'},
    cost=11.5,
    project_id='5599',
    created_at=now,
    updated_at=now,
)

test_bid_2 = bid.Bid(
    marketplace_bid_id='test_bid_2',
    creator_bid_id="2345",
    quantity=2,
    start_time=now,
    end_time=now,
    duration=16400,
    status="available",
    config_query={'foo': 'bar'},
    cost=11.5,
    project_id='5599',
    created_at=now,
    updated_at=now,
)

scoped_context = ctx.RequestContext(is_admin=False,
                                    project_id='5599')


@mock.patch('flocx_market.objects.bid.Bid.get_all')
def test_get_bids(mock_get_all, client):
    test_result = [test_bid_1, test_bid_2]
    mock_get_all.return_value = test_result
    response = client.get("/bid", follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 2


@mock.patch('flocx_market.objects.bid.Bid.get')
def test_get_bid(mock_get, client):
    mock_get.return_value = test_bid_1
    response = client.get('/bid/{}'.format(
        test_bid_1.marketplace_bid_id))
    assert response.status_code == 200
    mock_get.assert_called_once()
    assert response.json['marketplace_bid_id'] == 'test_bid_1'


@mock.patch('flocx_market.api.bid.bid.Bid.get')
def test_get_bid_missing(mock_get, client):
    mock_get.side_effect = e.ResourceNotFound()
    response = client.get('/bid/does-not-exist')
    assert(response.status_code == 404)


@mock.patch('flocx_market.objects.bid.Bid.destroy')
@mock.patch('flocx_market.objects.bid.Bid.get')
def test_delete_bid(mock_get, mock_destroy, client):
    mock_get.return_value = test_bid_1
    response = client.delete('/bid/{}'.format(
        test_bid_1.marketplace_bid_id))
    assert response.status_code == 200
    assert mock_destroy.call_count == 1


@mock.patch('flocx_market.objects.bid.Bid.get')
def test_delete_bid_missing(mock_get, client):
    mock_get.side_effect = e.ResourceNotFound()
    response = client.delete('/bid/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.objects.bid.Bid.create')
def test_create_bid(mock_create, client):
    mock_create.return_value = test_bid_1
    res = client.post('/bid', data=json.dumps(test_bid_1.to_dict()))
    assert res.status_code == 201
    assert mock_create.call_count == 1
    assert res.json == test_bid_1.to_dict()


@mock.patch('flocx_market.objects.bid.Bid.save')
@mock.patch('flocx_market.objects.bid.Bid.get')
def test_update_bid(mock_get, mock_save, client):
    mock_get.return_value = test_bid_1
    mock_save.return_value = test_bid_1
    res = client.put('/bid/{}'.format(test_bid_1.marketplace_bid_id),
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 200
    assert mock_save.call_count == 1


@mock.patch('flocx_market.objects.bid.Bid.save')
@mock.patch('flocx_market.objects.bid.Bid.get')
def test_update_bid_missing(mock_get, mock_save, client):
    mock_get.side_effect = e.ResourceNotFound()
    res = client.put('/bid/does-not-exist',
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 404
    assert mock_save.call_count == 0
