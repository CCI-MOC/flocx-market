from datetime import datetime

from flocx_market.objects import offer_contract_relationship as ocr
import unittest.mock as mock
from oslo_context import context as ctx

now = datetime.utcnow()


test_ocr_dict = dict(
    offer_contract_relationship_id='test_offer_contract_relationship_id',
    contract_id='test_contract_1',
    marketplace_offer_id='test_offer_1',
    status='unretrieved',
    created_at=now,
    updated_at=now,
)

scoped_context = ctx.RequestContext(is_admin=False,
                                    project_id='5599')


@mock.patch('flocx_market.db.sqlalchemy.api.offer_contract_relationship_get')
def test_get_by_id(offer_contract_relationship_get):
    offer_contract_relationship_get.return_value = test_ocr_dict
    ocr.OfferContractRelationship(**test_ocr_dict)
    ocr.OfferContractRelationship.get(scoped_context,
                                      'test_offer_contract_relationship_id')
    offer_contract_relationship_get.assert_called_once()


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_get_all')
def test_get_all_with_vals(offer_contract_relationship_get_all):
    offer_contract_relationship_get_all.return_value = [test_ocr_dict]
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    filters = {
        'marketplace_offer_id': oc.marketplace_offer_id,
        'contract_id': oc.contract_id,
        'status': oc.status
    }
    ocr.OfferContractRelationship.get_all(scoped_context, filters)
    offer_contract_relationship_get_all.assert_called_once()


def test_get_invalid():
    ret = ocr.OfferContractRelationship.get(scoped_context, 'does-not-exist')
    assert ret is None


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_get_all')
def test_get_all(offer_contract_relationship_get_all):
    ocr.OfferContractRelationship.get_all(scoped_context)
    offer_contract_relationship_get_all.assert_called_once()


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_destroy')
def test_destroy(offer_contract_relationship_destroy):
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.destroy(scoped_context)
    offer_contract_relationship_destroy.assert_called_once()


@mock.patch(
    'flocx_market.db.sqlalchemy.api.offer_contract_relationship_update')
def test_save(offer_contract_relationship_update):
    offer_contract_relationship_update.return_value = test_ocr_dict
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.status = "retrieved"
    oc.save(scoped_context)
    offer_contract_relationship_update.assert_called_once()


@mock.patch(
    'flocx_market.objects.offer_contract_relationship'
    '.OfferContractRelationship._from_db_object_list')
@mock.patch(
    'flocx_market.objects.offer_contract_relationship.db'
    '.offer_contract_relationship_get_all_unexpired')
def test_update_to_expire(get_all, _from_db_object_list):
    ocr.OfferContractRelationship.get_all_unexpired(scoped_context)
    get_all.assert_called_once()


@mock.patch('flocx_market.objects.offer_contract_relationship'
            '.OfferContractRelationship.save')
def test_expire(save):
    oc = ocr.OfferContractRelationship(**test_ocr_dict)
    oc.expire(scoped_context)

    save.assert_called_once()
