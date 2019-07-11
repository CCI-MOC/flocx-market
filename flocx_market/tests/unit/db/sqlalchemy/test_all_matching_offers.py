from flocx_market.db.sqlalchemy.offer_api import OfferApi
import datetime
from flocx_market.matcher import get_all_offers_matching_specs
now = datetime.datetime.utcnow()


def test_0_match(app, db, session):
    assert len(get_all_offers_matching_specs(
        [["memory", "==", 204]])) == 0


def test_1_match(app, db, session):
    test_offer_data = dict(
        provider_id='2345',
        creator_id='3456',
        marketplace_date_created=now,
        status='available',
        server_id='4567',
        start_time=now,
        end_time=now,
        server_config={'memory': 204},
        cost=0.0,)
    offer = OfferApi(**test_offer_data)
    offer.save_to_db()
    assert len(get_all_offers_matching_specs(
        [["memory", "==", 204]])) == 1


def test_only_1_match(app, db, session):
    test_offer_data = dict(
        provider_id='2345',
        creator_id='3456',
        marketplace_date_created=now,
        status='available',
        server_id='1',
        start_time=now,
        end_time=now,
        server_config={'memory': 202},
        cost=0.0,)
    offer = OfferApi(**test_offer_data)
    offer.save_to_db()

    test_offer_data = dict(
        provider_id='2345',
        creator_id='3456',
        marketplace_date_created=now,
        status='available',
        server_id='2',
        start_time=now,
        end_time=now,
        server_config={'memory': 204},
        cost=0.0,)
    offer = OfferApi(**test_offer_data)
    offer.save_to_db()
    assert len(get_all_offers_matching_specs(
        [["memory", "==", 204]])) == 1


def test_2_match(app, db, session):
    test_offer_data = dict(
        provider_id='2345',
        creator_id='3456',
        marketplace_date_created=now,
        status='available',
        server_id='1',
        start_time=now,
        end_time=now,
        server_config={'memory': 204},
        cost=0.0,)
    offer = OfferApi(**test_offer_data)
    offer.save_to_db()

    test_offer_data = dict(
        provider_id='2345',
        creator_id='3456',
        marketplace_date_created=now,
        status='available',
        server_id='2',
        start_time=now,
        end_time=now,
        server_config={'memory': 204},
        cost=0.0,)
    offer = OfferApi(**test_offer_data)
    offer.save_to_db()
    assert len(get_all_offers_matching_specs(
        [["memory", "==", 204]])) == 2
