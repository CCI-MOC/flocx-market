from flocx_market.objects import offer_contract_relationship as ocr
import unittest.mock as mock

test_ocr_dict = dict(
    offer_contract_relationship_id='test_offer_contract_relationship_id',
    contract_id='test_contract_1',
    marketplace_offer_id='test_offer_1',
    status='unretrieved')


@mock.patch('flocx_market.db.sqlalchemy.api.offer_contract_relationship_get')
def test_get(offer_contract_relationship_get):
    offer_contract_relationship_get.return_value = test_ocr_dict
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    ocr.OfferContractRelationship.get(oc.contract_id, oc.marketplace_offer_id)
    offer_contract_relationship_get.assert_called_once()


def test_get_none():
    ret = ocr.OfferContractRelationship.get(None, None)
    assert ret is None


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_get_all')
def test_get_all(offer_contract_relationship_get_all):
    ocr.OfferContractRelationship.get_all()
    offer_contract_relationship_get_all.assert_called_once()


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_destroy')
def test_destroy(offer_contract_relationship_destroy):
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.destroy()
    offer_contract_relationship_destroy.assert_called_once()


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_update')
def test_save(offer_contract_relationship_update):
    offer_contract_relationship_update.return_value = test_ocr_dict
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.status = "retrieved"
    oc.save()
    offer_contract_relationship_update.assert_called_once()


@mock.patch(
    'flocx_market.objects.offer_contract_relationship'
    '.OfferContractRelationship._from_db_object_list')
@mock.patch(
    'flocx_market.objects.offer_contract_relationship.db'
    '.offer_contract_relationship_get_all_unexpired')
def test_update_to_expire(get_all, _from_db_object_list):
    ocr.OfferContractRelationship.get_all_unexpired()
    get_all.assert_called_once()


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.save')
def test_expire(save):
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.expire()

    save.assert_called_once()
