from flocx_market.models.offer import OfferModel
from flocx_market.tests.base_test import BaseTest


class TestOffer(BaseTest):
    def test_crud(self):
        with self.app_context():
            offer = OfferModel('b711b1ca-a77e-4392-a9b5-dc84c4f469ac', 'b9752cc0-9bed-4f1c-8917-12ade7a6fdbe', 'Alice1992',
                           '2016-07-16T19:20:30', 'available', 'Dell380', '2016-07-16T19:20:30', '2016-08-16T19:20:30',
                           '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                           11.5)
            self.assertIsNone(OfferModel.find_by_id('b711b1ca-a77e-4392-a9b5-dc84c4f469ac'))
            offer.save_to_db()
            self.assertIsNotNone(OfferModel.find_by_id('b711b1ca-a77e-4392-a9b5-dc84c4f469ac'))
            offer.delete_from_db()
            self.assertIsNone(OfferModel.find_by_id('b711b1ca-a77e-4392-a9b5-dc84c4f469ac'))