import datetime
import json
from unittest import mock

import flocx_market.conf
from flocx_market.objects import offer


CONF = flocx_market.conf.CONF

now = datetime.datetime.utcnow()


test_offer_1 = offer.Offer(
    marketplace_date_created=now,
    marketplace_offer_id='test_offer_1',
    provider_id='1234',
    creator_id='2345',
    server_id='3456',
    start_time=now,
    end_time=now,
    status='available',
    server_config={'bar': 'foo'},
    cost=0.0,
)

test_offer_2 = offer.Offer(
    marketplace_offer_id='test_offer_2',
    marketplace_date_created=now,
    provider_id='2345',
    creator_id='3456',
    server_id='4567',
    start_time=now,
    end_time=now,
    status='available',
    server_config={'foo': 'bar'},
    cost=0.0,
)


@mock.patch('flocx_market.objects.offer.Offer.get_all')
def test_get_offers(mock_get_all, client):
    test_result = [test_offer_1, test_offer_2]
    mock_get_all.return_value = test_result
    response = client.get("/offer", follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 2
    assert any(x['provider_id'] == test_offer_1.provider_id
               for x in response.json)
    assert any(x['provider_id'] == test_offer_2.provider_id
               for x in response.json)


@mock.patch('flocx_market.objects.offer.Offer.get')
def test_get_offer(mock_get, client):
    mock_get.return_value = test_offer_1
    response = client.get('/offer/{}'.format(
        test_offer_1.marketplace_offer_id))
    assert response.status_code == 200
    mock_get.assert_called_with('test_offer_1')
    assert response.json['marketplace_offer_id'] == 'test_offer_1'


@mock.patch('flocx_market.objects.offer.Offer.get')
def test_get_offer_missing(mock_get, client):
    mock_get.return_value = None
    response = client.get('/offer/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.objects.offer.Offer.destroy')
@mock.patch('flocx_market.objects.offer.Offer.get')
def test_delete_offer(mock_get, mock_destroy, client):
    mock_get.return_value = test_offer_1
    response = client.delete('/offer/{}'.format(
        test_offer_1.marketplace_offer_id))
    assert response.status_code == 200
    assert mock_destroy.call_count == 1


@mock.patch('flocx_market.objects.offer.Offer.get')
def test_delete_offer_missing(mock_get, client):
    mock_get.return_value = None
    response = client.delete('/offer/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.objects.offer.Offer.create')
def test_create_offer(mock_create, client):
    mock_create.return_value = test_offer_1
    res = client.post('/offer', data=json.dumps(test_offer_1.to_dict()))
    assert res.status_code == 201
    assert mock_create.call_count == 1
    assert res.json == test_offer_1.to_dict()


@mock.patch('flocx_market.objects.offer.Offer.save')
@mock.patch('flocx_market.objects.offer.Offer.get')
def test_update_offer(mock_get, mock_save, client):
    mock_get.return_value = test_offer_1
    mock_save.return_value = test_offer_1
    res = client.put('/offer/{}'.format(test_offer_1.marketplace_offer_id),
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 200
    assert mock_save.call_count == 1


@mock.patch('flocx_market.objects.offer.Offer.save')
@mock.patch('flocx_market.objects.offer.Offer.get')
def test_update_offer_missing(mock_get, mock_save, client):
    mock_get.return_value = None
    res = client.put('/offer/does-not-exist',
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 404
    assert mock_save.call_count == 0
