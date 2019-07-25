import datetime
import json
from unittest import mock

import flocx_market.conf
from flocx_market.objects import bid, offer, contract, \
    offer_contract_relationship as ocr
CONF = flocx_market.conf.CONF
now = datetime.datetime.utcnow()

contract_1_bid = bid.Bid(marketplace_bid_id='test_bid_1',
                         creator_bid_id="1234",
                         server_quantity=2,
                         start_time=now,
                         end_time=now,
                         duration=16400,
                         status="available",
                         server_config_query={'foo': 'bar'},
                         cost=11.5,
                         project_id='5599'
                         )

contract_2_bid = bid.Bid(marketplace_bid_id='test_bid_2',
                         creator_bid_id="2345",
                         server_quantity=2,
                         start_time=now,
                         end_time=now,
                         duration=16400,
                         status="available",
                         server_config_query={'foo': 'bar'},
                         cost=11.5,
                         project_id='5599'
                         )

contract_1_offer = offer.Offer(marketplace_date_created=now,
                               marketplace_offer_id='test_offer_1',
                               provider_id='1234',
                               server_id='3456',
                               start_time=now,
                               end_time=now,
                               status='available',
                               server_config={'bar': 'foo'},
                               cost=0.0,
                               contract_id='test_contract_1',
                               project_id='5599'
                               )

contract_2_offer = offer.Offer(marketplace_offer_id='test_offer_2',
                               marketplace_date_created=now,
                               provider_id='2345',
                               server_id='4567',
                               start_time=now,
                               end_time=now,
                               status='available',
                               server_config={'foo': 'bar'},
                               cost=0.0,
                               contract_id='test_contract_2',
                               project_id='5599'

                               )

test_contract_1 = contract.Contract(contract_id='test_contract_1',
                                    time_created=now,
                                    status='available',
                                    start_time=now,
                                    end_time=now,
                                    cost=0.0,
                                    bid_id='test_bid_1',
                                    bid=None,
                                    project_id='5599'
                                    )

test_contract_2 = contract.Contract(contract_id='test_contract_2',
                                    time_created=now,
                                    status='available',
                                    start_time=now,
                                    end_time=now,
                                    cost=0.0,
                                    bid_id='test_bid_2',
                                    bid=None,
                                    project_id='5599'
                                    )

test_contract_dict = dict(contract_id='test_contract_2',
                          time_created="2016-07-16T19:20:30",
                          status='available',
                          start_time="2016-07-16T19:20:30",
                          end_time="2016-07-16T19:20:30",
                          cost=0.0,
                          bid_id='test_bid_2',
                          offers=[contract_1_offer.marketplace_offer_id],
                          project_id='5599'
                          )

test_ocr_1 = ocr.OfferContractRelationship(
                offer_contract_relationship_id='test_ocr_id_1',
                marketplace_offer_id='test_offer_1',
                contract_id='test_contract_1',
                status='unretrieved')

test_ocr_2 = ocr.OfferContractRelationship(
            offer_contract_relationship_id='test_ocr_id_2',
            marketplace_offer_id='test_offer_2',
            contract_id='test_contract_2',
            status='unretrieved')


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get_all')
def test_get_offer_contract_relationships(mock_get_all, client):
    test_result = [test_ocr_1, test_ocr_2]
    mock_get_all.return_value = test_result
    response = client.get("/offer_contract_relationship",
                          follow_redirects=True)
    assert response.status_code == 200
    assert len(response.json) == 2
    assert any(x['contract_id'] == test_ocr_1.contract_id
               for x in response.json)
    assert any(x['contract_id'] == test_ocr_2.contract_id
               for x in response.json)


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get')
def test_get_offer_contract_relationship(mock_get, client):
    mock_get.return_value = test_ocr_1
    response = client.get('/offer_contract_relationship/{}/{}'.format(
        test_ocr_1.marketplace_offer_id, test_ocr_1.contract_id))
    print(response.data)
    assert response.status_code == 200
    mock_get.assert_called_with('test_offer_1', 'test_contract_1')
    assert response.json['offer_contract_relationship_id'] == 'test_ocr_id_1'


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get')
def test_get_offer_contract_relationship_missing(mock_get, client):
    mock_get.return_value = None
    response = client.get('/offer_contract_relationship/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.destroy')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get')
def test_delete_offer_contract_relationship(mock_get, mock_destroy, client):
    mock_get.return_value = test_ocr_1
    response = client.delete('/offer_contract_relationship/{}/{}'.format(
        test_ocr_1.marketplace_offer_id, test_ocr_1.contract_id))
    assert response.status_code == 200
    assert mock_destroy.call_count == 1


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get')
def test_delete_offer_contract_relationship_missing(mock_get, client):
    mock_get.return_value = None
    response = client.delete('/offer_contract_relationship/does-not-exist')
    assert response.status_code == 404


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.save')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get')
def test_update_offer_contract_relationship(mock_get, mock_save, client):
    mock_get.return_value = test_ocr_1
    mock_save.return_value = test_ocr_1
    res = client.put('/offer_contract_relationship/{}/{}'.format(
        test_ocr_1.marketplace_offer_id, test_ocr_1.contract_id),
        data=json.dumps(dict(status='testing')))
    assert res.status_code == 200
    assert mock_save.call_count == 1
    assert res.json['status'] == 'testing'


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.save')
@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.get')
def test_update_offer_contract_relationship_missing(mock_get,
                                                    mock_save, client):
    mock_get.return_value = None
    res = client.put('/offer_contract_relationship/does-not-exist',
                     data=json.dumps(dict(status='testing')))
    assert res.status_code == 404
    assert mock_save.call_count == 0
