from oslo_db.sqlalchemy import session as db_session
from oslo_utils import uuidutils

import flocx_market.conf
from flocx_market.db.sqlalchemy import models
from flocx_market.common import exception

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

    offer_ref = get_session().query(models.Offer).filter_by(
            marketplace_offer_id=marketplace_offer_id).one_or_none()

    if offer_ref:
        return offer_ref
    else:
        raise exception.ResourceNotFound(resource_type="Offer",
                                         resource_uuid=marketplace_offer_id)


def offer_get_all(context):
    return get_session().query(models.Offer).all()


def offer_get_all_by_project_id(context):
    return get_session().query(models.Offer).filter_by(
        project_id=context.project_id).all()


def offer_get_all_by_server_id(context, server_id, status=None):
    query = get_session().query(models.Offer).filter_by(
        server_id=server_id)
    if status is not None:
        query = query.filter_by(status=status)
    return query.all()


def offer_get_all_unexpired(context):
    if context.is_admin:
        return get_session().query(models.Offer).filter(
            models.Offer.status != 'expired').all()
    else:
        return get_session().query(models.Offer).filter(
            models.Offer.status != 'expired',
            models.Offer.project_id == context.project_id).all()


def offer_get_all_by_status(status, context):
    if context.is_admin:
        return get_session().query(models.Offer)\
                            .filter_by(status=status).all()
    return get_session().query(models.Offer)\
        .filter(models.Offer.status == status, models.Offer.project_id ==
                context.project_id).all()


def offer_create(values, context):

    server_id = values['server_id']
    if len(offer_get_all_by_server_id(context, server_id, 'available')) > 0:
        raise ValueError(
            "Node %server_id already has an available offer",
            server_id
        )

    values['marketplace_offer_id'] = uuidutils.generate_uuid()
    offer_ref = models.Offer()
    offer_ref.update(values)
    offer_ref.save(get_session())
    return offer_ref


def offer_update(marketplace_offer_id, values, context):

    if context.is_admin:
        offer_ref = get_session().query(models.Offer).filter_by(
                    marketplace_offer_id=marketplace_offer_id).one_or_none()
    else:
        offer_ref = get_session().query(models.Offer).filter_by(
            marketplace_offer_id=marketplace_offer_id).one_or_none()

    if offer_ref:
        if offer_ref.project_id != context.project_id and not context.is_admin:
            raise exception.ResourceNoPermission(
                                            resource_type="Offer",
                                            resource_uuid=marketplace_offer_id)
        values.pop('marketplace_offer_id', None)
        offer_ref.update(values)
        offer_ref.save(get_session())
        return offer_ref
    else:
        raise exception.ResourceNotFound(resource_type="Offer",
                                         resource_uuid=marketplace_offer_id)


def offer_destroy(marketplace_offer_id, context):
    if context.is_admin:
        offer_ref = get_session().query(models.Offer).filter_by(
                    marketplace_offer_id=marketplace_offer_id).one_or_none()
    else:
        offer_ref = get_session().query(models.Offer).filter_by(
            marketplace_offer_id=marketplace_offer_id).one_or_none()

    if offer_ref:
        if offer_ref.project_id != context.project_id and not context.is_admin:
            raise exception.ResourceNoPermission(
                                            resource_type="Offer",
                                            resource_uuid=marketplace_offer_id)

        if context.is_admin:
            get_session().query(models.Offer).filter_by(
                marketplace_offer_id=marketplace_offer_id).delete()
        else:
            get_session().query(models.Offer).filter_by(
                marketplace_offer_id=marketplace_offer_id,
                project_id=context.project_id).delete()
    else:
        raise exception.ResourceNotFound(resource_type="Offer",
                                         resource_uuid=marketplace_offer_id)


def bid_get(marketplace_bid_id, context):

    bid_ref = get_session().query(models.Bid).filter_by(
        marketplace_bid_id=marketplace_bid_id).one_or_none()

    if bid_ref:
        return bid_ref
    else:
        raise exception.ResourceNotFound(resource_type="Bid",
                                         resource_uuid=marketplace_bid_id)


def bid_get_all(context):
    return get_session().query(models.Bid).all()


def bid_get_all_by_project_id(context):
    return get_session().query(models.Bid)\
        .filter_by(project_id=context.project_id).all()


def bid_get_all_unexpired(context):
    return get_session().query(models.Bid)\
        .filter(models.Bid.status != 'expired').all()


def bid_get_all_by_status(status, context):
    if context.is_admin:
        return get_session().query(models.Bid)\
                            .filter_by(status=status).all()
    return get_session().query(models.Bid)\
        .filter(models.Bid.status == status, models.Bid.project_id ==
                context.project_id).all()


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
                    marketplace_bid_id=marketplace_bid_id).one_or_none()
    else:
        bid_ref = get_session().query(models.Bid).filter_by(
            marketplace_bid_id=marketplace_bid_id).one_or_none()

    if bid_ref:
        if bid_ref.project_id != context.project_id and not context.is_admin:
            raise exception.ResourceNoPermission(
                                            resource_type="Bid",
                                            resource_uuid=marketplace_bid_id)

        values.pop('marketplace_bid_id', None)
        bid_ref.update(values)
        bid_ref.save(get_session())
        return bid_ref
    else:
        raise exception.ResourceNotFound(resource_type="Bid",
                                         resource_uuid=marketplace_bid_id)


def bid_destroy(marketplace_bid_id, context):
    if context.is_admin:
        bid_ref = get_session().query(models.Bid).filter_by(
                    marketplace_bid_id=marketplace_bid_id).one_or_none()
    else:
        bid_ref = get_session().query(models.Bid).filter_by(
            marketplace_bid_id=marketplace_bid_id).one_or_none()

    if bid_ref:
        if bid_ref.project_id != context.project_id and not context.is_admin:
            raise exception.ResourceNoPermission(
                                            resource_type="Bid",
                                            resource_uuid=marketplace_bid_id)

        if context.is_admin:
            get_session().query(models.Bid).filter_by(
                marketplace_bid_id=marketplace_bid_id).delete()
        else:
            get_session().query(models.Bid).filter_by(
                marketplace_bid_id=marketplace_bid_id,
                project_id=context.project_id).delete()
    else:
        raise exception.ResourceNotFound(resource_type="Bid",
                                         resource_uuid=marketplace_bid_id)


# contract
def contract_get(contract_id, context):

    contract_ref = get_session().query(models.Contract).filter_by(
        contract_id=contract_id).one_or_none()

    if contract_ref:
        return contract_ref
    else:
        raise exception.ResourceNotFound(resource_type="Contract",
                                         resource_uuid=contract_id)


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
        raise exception.RequiresAdmin(
            resource_type="Contract")


def contract_update(contract_id, values, context):

    if context.is_admin:
        contract_ref = get_session().query(models.Contract).filter_by(
                        contract_id=contract_id).one_or_none()
        if contract_ref:
            values.pop('contract_id', None)
            contract_ref.update(values)
            contract_ref.save(get_session())
            return contract_ref
        else:
            raise exception.ResourceNotFound(resource_type="Contract",
                                             resource_uuid=contract_id)
    else:
        raise exception.ResourceNoPermission(resource_type="Contract",
                                             resource_uuid=contract_id)


def contract_destroy(contract_id, context):
    if context.is_admin:
        contract_ref = contract_get(contract_id, context)
        if contract_ref:
            get_session().query(models.Contract).filter_by(
                contract_id=contract_id).delete()
        else:
            raise exception.ResourceNotFound(resource_type="Contract",
                                             resource_uuid=contract_id)
    else:
        raise exception.ResourceNoPermission(resource_type="Contract",
                                             resource_uuid=contract_id)


# offer_contract_relationship
def offer_contract_relationship_get(context,
                                    offer_contract_relationship_id=None):

    if offer_contract_relationship_id is None:
        return None

    ref = get_session().query(models.OfferContractRelationship).filter(
        models.OfferContractRelationship.offer_contract_relationship_id
        == offer_contract_relationship_id).one_or_none()
    if ref:
        return ref
    else:
        raise exception.ResourceNotFound(
            resource_type="Offer_Contract_Relationship",
            resource_uuid=offer_contract_relationship_id)


def offer_contract_relationship_get_all(context, filters=None):
    query = get_session().query(models.OfferContractRelationship)
    if filters is not None:
        for field in ['marketplace_offer_id', 'contract_id', 'status']:
            if field in filters:
                query = query.filter_by(**{field: filters[field]})
    return query.all()


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
        raise exception.RequiresAdmin(
            resource_type="Offer_Contract_Relationship")


def offer_contract_relationship_update(context,
                                       offer_contract_relationship_id,
                                       values):
    offer_contract_relationship_ref \
        = offer_contract_relationship_get(context,
                                          offer_contract_relationship_id)

    values.pop('offer_contract_relationship_id', None)
    offer_contract_relationship_ref.update(values)
    offer_contract_relationship_ref.save(get_session())
    return offer_contract_relationship_ref


def offer_contract_relationship_destroy(context,
                                        offer_contract_relationship_id):
    if context.is_admin:
        offer_contract_relationship_ref \
            = offer_contract_relationship_get(context,
                                              offer_contract_relationship_id)

        if offer_contract_relationship_ref:
            get_session().query(models.OfferContractRelationship) \
                .filter(models.OfferContractRelationship.
                        offer_contract_relationship_id ==
                        offer_contract_relationship_id).delete()
        else:
            return None
    else:
        raise exception.RequiresAdmin(
            resource_type="Offer_Contract_Relationship")
