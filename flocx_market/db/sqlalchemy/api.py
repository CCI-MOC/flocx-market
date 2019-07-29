from oslo_db.sqlalchemy import session as db_session
from oslo_utils import uuidutils

import flocx_market.conf
from flocx_market.db.sqlalchemy import models

CONF = flocx_market.conf.CONF
_engine_facade = None


def get_facade():
    global _engine_facade
    if not _engine_facade:
        _engine_facade = db_session.EngineFacade.from_config(CONF)

    return _engine_facade


def get_session():
    return get_facade().get_session()


def reset_facade():
    global _engine_facade
    _engine_facade = None


def setup_db():
    engine = get_facade().get_engine()
    models.Base.metadata.create_all(engine)
    return True


def drop_db():
    engine = db_session.EngineFacade(CONF.database.connection,
                                     sqlite_fk=True).get_engine()
    models.Base.metadata.drop_all(engine)
    return True


def offer_get(marketplace_offer_id, context):

    return get_session().query(models.Offer).filter_by(
            marketplace_offer_id=marketplace_offer_id).first()


def offer_get_all(context):
    return get_session().query(models.Offer).all()


def offer_get_all_by_project_id(context):
    return get_session().query(models.Offer).filter_by(
        project_id=context.project_id).all()


def offer_get_all_unexpired(context):

    if context.is_admin:
        return get_session().query(models.Offer).filter(
            models.Offer.status != 'expired').all()
    else:
        return get_session().query(models.Offer).filter(
            models.Offer.status != 'expired',
            models.Offer.project_id == context.project_id).all()


def offer_create(values, context):
    values['marketplace_offer_id'] = uuidutils.generate_uuid()
    values['project_id'] = context.project_id
    offer_ref = models.Offer()
    offer_ref.update(values)
    offer_ref.save(get_session())
    return offer_ref


def offer_update(marketplace_offer_id, values, context):

    if context.is_admin:
        offer_ref = get_session().query(models.Offer).filter_by(
                    marketplace_offer_id=marketplace_offer_id).first()
    else:
        offer_ref = get_session().query(models.Offer).filter_by(
            marketplace_offer_id=marketplace_offer_id,
            project_id=context.project_id).first()

    if offer_ref:
        values.pop('marketplace_offer_id', None)
        offer_ref.update(values)
        offer_ref.save(get_session())
        return offer_ref
    else:
        return None


def offer_destroy(marketplace_offer_id, context):
    if context.is_admin:
        offer_ref = get_session().query(models.Offer).filter_by(
                    marketplace_offer_id=marketplace_offer_id).first()
    else:
        offer_ref = get_session().query(models.Offer).filter_by(
            marketplace_offer_id=marketplace_offer_id,
            project_id=context.project_id).first()

    if offer_ref:

        if context.is_admin:
            get_session().query(models.Offer).filter_by(
                marketplace_offer_id=marketplace_offer_id).delete()
        else:
            get_session().query(models.Offer).filter_by(
                marketplace_offer_id=marketplace_offer_id,
                project_id=context.project_id).delete()
    else:
        return None


def bid_get(marketplace_bid_id, context):
    return get_session().query(models.Bid).filter_by(
        marketplace_bid_id=marketplace_bid_id).first()


def bid_get_all(context):
    return get_session().query(models.Bid).all()


def bid_get_all_by_project_id(context):
    return get_session().query(models.Bid)\
        .filter_by(project_id=context.project_id).all()


def bid_get_all_unexpired(context):
    return get_session().query(models.Bid)\
        .filter(models.Bid.status != 'expired').all()


def bid_create(values, context):
    values['marketplace_bid_id'] = uuidutils.generate_uuid()
    values['project_id'] = context.project_id
    bid_ref = models.Bid()
    bid_ref.update(values)
    bid_ref.save(get_session())
    return bid_ref


def bid_update(marketplace_bid_id, values, context):
    if context.is_admin:
        bid_ref = get_session().query(models.Bid).filter_by(
                    marketplace_bid_id=marketplace_bid_id).first()
    else:
        bid_ref = get_session().query(models.Bid).filter_by(
            marketplace_bid_id=marketplace_bid_id,
            project_id=context.project_id).first()

    if bid_ref:
        values.pop('marketplace_bid_id', None)
        bid_ref.update(values)
        bid_ref.save(get_session())
        return bid_ref
    else:
        return None


def bid_destroy(marketplace_bid_id, context):
    if context.is_admin:
        bid_ref = get_session().query(models.Bid).filter_by(
                    marketplace_bid_id=marketplace_bid_id).first()
    else:
        bid_ref = get_session().query(models.Bid).filter_by(
            marketplace_bid_id=marketplace_bid_id,
            project_id=context.project_id).first()

    if bid_ref:

        if context.is_admin:
            get_session().query(models.Bid).filter_by(
                marketplace_bid_id=marketplace_bid_id).delete()
        else:
            get_session().query(models.Bid).filter_by(
                marketplace_bid_id=marketplace_bid_id,
                project_id=context.project_id).delete()
    else:
        return None


# contract
def contract_get(contract_id, context):
    return get_session().query(models.Contract).filter_by(
        contract_id=contract_id).first()


def contract_get_all(context):
    return get_session().query(models.Contract).all()


def contract_get_all_unexpired(context):
    return get_session().query(models.Contract)\
        .filter(models.Contract.status != 'expired').all()


def contract_create(values, context):

    if context.is_admin:
        values['contract_id'] = uuidutils.generate_uuid()
        # exception for foreign key constraint needed here
        offers = values['offers']

        del values['offers']
        contract_ref = models.Contract()
        contract_ref.update(values)
        contract_ref.save(get_session())

        # update foreign key for offers
        for offer_id in offers:
            ocr_data = dict(contract_id=values['contract_id'],
                            marketplace_offer_id=offer_id,
                            status='unretrieved')
            offer_contract_relationship_create(context, ocr_data)
        return contract_ref
    else:
        return None


def contract_update(contract_id, values, context):

    if context.is_admin:
        contract_ref = get_session().query(models.Contract).filter_by(
                        contract_id=contract_id).first()
        if contract_ref:
            values.pop('contract_id', None)
            contract_ref.update(values)
            contract_ref.save(get_session())
            return contract_ref
        else:
            return None
    else:
        return None


def contract_destroy(contract_id, context):
    if context.is_admin:
        contract_ref = contract_get(contract_id, context)
        if contract_ref:
            get_session().query(models.Contract).filter_by(
                contract_id=contract_id).delete()
        else:
            return None
    else:
        return None


# offer_contract_relationship
def offer_contract_relationship_get(context,
                                    contract_id=None,
                                    marketplace_offer_id=None):

    if (contract_id is not None) and (marketplace_offer_id is None):
        return get_session().query(models.OfferContractRelationship).filter_by(
            contract_id=contract_id).all()

    elif (contract_id is None) and (marketplace_offer_id is not None):
        return get_session().query(models.OfferContractRelationship).filter_by(
            marketplace_offer_id=marketplace_offer_id).all()
    elif (contract_id is not None) and (marketplace_offer_id is not None):
        return get_session().query(models.OfferContractRelationship) \
            .filter(models.OfferContractRelationship.contract_id
                    == contract_id,
                    models.OfferContractRelationship.marketplace_offer_id
                    == marketplace_offer_id).first()


def offer_contract_relationship_get_all(context):
    return get_session().query(models.OfferContractRelationship).all()


def offer_contract_relationship_get_all_unexpired(context):
    return get_session().query(models.OfferContractRelationship)\
        .filter(models.OfferContractRelationship.status != 'expired').all()


def offer_contract_relationship_create(context, values):

    if context.is_admin:
        values['offer_contract_relationship_id'] = uuidutils.generate_uuid()
        # exception for foreign key constraint needed here
        offer_contract_relationship_ref = models.OfferContractRelationship()
        offer_contract_relationship_ref.update(values)
        offer_contract_relationship_ref.save(get_session())
        return offer_contract_relationship_ref
    else:
        return None


def offer_contract_relationship_update(context,
                                       contract_id,
                                       marketplace_offer_id,
                                       values):
    if context.is_admin:
        offer_contract_relationship_ref = offer_contract_relationship_get(
            context,
            contract_id=contract_id,
            marketplace_offer_id=marketplace_offer_id)

        values.pop('contract_id', None)
        values.pop('marketplace_offer_id', None)
        offer_contract_relationship_ref.update(values)
        offer_contract_relationship_ref.save(get_session())
        return offer_contract_relationship_ref
    else:
        return None


def offer_contract_relationship_destroy(context,
                                        contract_id,
                                        marketplace_offer_id):
    if context.is_admin:
        offer_contract_relationship_ref = offer_contract_relationship_get(
                                            context,
                                            contract_id,
                                            marketplace_offer_id)

        if offer_contract_relationship_ref:
            get_session().query(models.OfferContractRelationship) \
                .filter(models.OfferContractRelationship.contract_id
                        == contract_id and
                        models.OfferContractRelationship.marketplace_offer_id
                        == marketplace_offer_id).delete()
        else:
            return None
    else:
        return None
