import datetime
import pytest
from flocx_market.db.sqlalchemy.bid_api import BidApi

from sqlalchemy.exc import IntegrityError


now = datetime.datetime.utcnow()
test_bid_data = dict(creator_bid_id="12a59a51-b4d6-497d-9f75-f56c409305c8",
                     creator_id="12a59a51-b4d6-497d-9f75-f56c409305c8",
                     server_quantity=2,
                     start_time=now,
                     end_time=now,
                     duration=16400,
                     status="available",
                     server_config_query={'foo': 'bar'},
                     cost=11.5)


def test_bid_create(app, db, session):
    bid = BidApi(**test_bid_data)
    bid.save_to_db()
    check = BidApi.find_by_id(bid.marketplace_bid_id)

    assert check.as_dict() == bid.as_dict()


def test_bid_create_invalid(app, db, session):
    del test_bid_data['creator_bid_id']
    bid = BidApi(**test_bid_data)

    with pytest.raises(IntegrityError):
        bid.save_to_db()
    test_bid_data['creator_bid_id'] = '12a59a51-b4d6-497d-9f75-f56c409305c8'


def test_bid_delete(app, db, session):
    bid = BidApi(**test_bid_data)
    bid.save_to_db()
    bid.delete_from_db()
    check = BidApi.find_by_id(bid.marketplace_bid_id)
    assert check is None
