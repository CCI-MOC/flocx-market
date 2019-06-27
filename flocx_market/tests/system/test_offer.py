from flocx_market.db.sqlalchemy.offer_api import OfferApi
from flocx_market.tests.base_test import BaseTest
import json


class TestOffer(BaseTest):
    def setUp(self):
        super(TestOffer, self).setUp()
        # perform auth in future
        pass

    def test_get_offer_not_found(self):
        with self.app() as client:
            with self.app_context():
                res = client.get('/offers/b711b1ca-a77e-4392-a9b5-dc84c4f469ac')
                self.assertEqual(res.status_code, 404)

    def test_get_offer(self):
        with self.app() as client:
            with self.app_context():
                offer = OfferApi('b9752cc0-9bed-4f1c-8917-12ade7a6fdbe',
                                 'Alice1992',
                                 '2016-07-16T19:20:30', 'available', 'Dell380', '2016-07-16T19:20:30',
                                 '2016-08-16T19:20:30',
                                 '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                                 11.5)
                offer.save_to_db()
                res = client.get(f'/offers/{offer.marketplace_offer_id}')
                self.assertEqual(res.status_code, 200)

    def test_delete_offer(self):
        with self.app() as client:
            with self.app_context():
                offer = OfferApi('b9752cc0-9bed-4f1c-8917-12ade7a6fdbe',
                                 'Alice1992',
                                 '2016-07-16T19:20:30', 'available', 'Dell380', '2016-07-16T19:20:30',
                                 '2016-08-16T19:20:30',
                                 '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                                 11.5)
                offer.save_to_db()
                res = client.delete(f'/offers/{offer.marketplace_offer_id}')
                self.assertEqual(res.status_code, 200)
                self.assertDictEqual({'message': 'Offer deleted.'}, json.loads(res.data))

    def test_create_offer(self):
        with self.app() as client:
            with self.app_context():
                offer = {"provider_id": "b9752cc0-9bed-4f1c-8917-12ade7a6fdbe",
                         "creator_id": "Alice1992",
                         "marketplace_date_created": "2016-07-16T19:20:30",
                         "status": "available",
                         "server_id": "Dell380",
                         "start_time": "2016-07-16T19:20:30",
                         "end_time": "2016-08-16T19:20:30",
                         "server_config": '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                         "cost": 11.5}
                res = client.post('/offer', data=offer)
                self.assertEqual(res.status_code, 201)

    '''def test_create_duplicate_offer(self):
        with self.app() as client:
            with self.app_context():
                offer1 = OfferModel('b9752cc0-9bed-4f1c-8917-12ade7a6fdbe',
                           'Alice1992',
                           '2016-07-16T19:20:30', 'available', 'Dell380', '2016-07-16T19:20:30',
                           '2016-08-16T19:20:30',
                           '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                           11.5).save_to_db()
                offer2 = {
                    "provider_id": "b9752cc0-9bed-4f1c-8917-12ade7a6fdbe",
                    "creator_id": "Alice1992",
                    "marketplace_date_created": "2016-07-16T19:20:30",
                    "status": "available",
                    "server_id": "Dell380",
                    "start_time": "2016-07-16T19:20:30",
                    "end_time": "2016-08-16T19:20:30",
                    "server_config": '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                    "cost": 11.5}
                res = client.post('/offer', data=offer2)
                self.assertEqual(res.status_code, 400)
                self.assertDictEqual({'message': "An offer with marketplace_offer_id \'b711b1ca-a77e-4392-a9b5-dc84c4f469ac\' already exists."},
                                     json.loads(res.data))'''

    def test_put_offer(self):
        with self.app() as client:
            with self.app_context():
                offer = OfferApi('b9752cc0-9bed-4f1c-8917-12ade7a6fdbe',
                                 'Alice1992',
                                 '2016-07-16T19:20:30', 'available', 'Dell380', '2016-07-16T19:20:30',
                                 '2016-08-16T19:20:30',
                                 '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                                 11.5)
                offer.save_to_db()
                res = client.put(f'/offers/{offer.marketplace_offer_id}', data={"status": "busy"})
                self.assertEqual(offer.status, "busy")
                self.assertEqual(res.status_code, 200)

    def test_offer_list(self):
        with self.app() as client:
            with self.app_context():
                OfferApi('b9752cc0-9bed-4f1c-8917-12ade7a6fdbe',
                         'Alice1992',
                         '2016-07-16T19:20:30', 'available', 'Dell380', '2016-07-16T19:20:30',
                         '2016-08-16T19:20:30',
                         '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                         11.5).save_to_db()
                res = client.get('/offers')
                self.assertEqual(res.status_code, 200)
