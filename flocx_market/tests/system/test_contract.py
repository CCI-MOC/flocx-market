from flocx_market.db.sqlalchemy.contract_api import ContractApi
from flocx_market.db.sqlalchemy.offer_api import OfferApi
from flocx_market.db.sqlalchemy.bid_api import BidApid
from flocx_market.tests.base_test import BaseTest
import json


class TestContract(BaseTest):
    def setUp(self):
        super(TestContract, self).setUp()
        # perform auth in future
        pass

    def test_create_contract(self):
        with self.app() as client:
            with self.app_context():
                offer = OfferApi("b9752cc0-9bed-4f1c-8917-12ade7a6fdbe",
                                 "Alice1992",
                                 "2016-07-16T19:20:30",
                                 "available", "Dell380",
                                 "2016-07-16T19:20:30",
                                 "2016-08-16T19:20:30",
                                 '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                                 11.5)
                offer.save_to_db()
                bid = BidApid("12a59a51-b4d6-497d-9f75-f56c409305c8",
                              "12a59a51-b4d6-497d-9f75-f56c409305c8",
                              2,
                              "(2016-07-16T19:20:30-04:00)",
                              "(2016-08-16T19:20:30-04:00)",
                              16400,
                              80,
                              '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                              11.5)
                bid.save_to_db()
                contract = {
                    "time_created": "2016-07-16T19:20:30",
                    "bid_id": f"{bid.marketplace_bid_id}",
                    "status": "available",
                    "start_time": "2016-07-16T19:20:30",
                    "end_time": "2016-07-16T19:20:30",
                    "cost": "11.5",
                    "offers": '{"1": "%s"}' % offer.marketplace_offer_id
                }
                res = client.post('/contract', data=contract)
                self.assertEqual(res.status_code, 201)
