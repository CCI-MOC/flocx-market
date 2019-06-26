from flocx_market.tests.unit.unit_base_test import UnitBaseTest
from flocx_market.models.offer import OfferModel


class TestOfferModel(UnitBaseTest):
    def test_create_offer(self):
        o = OfferModel('b711b1ca-a77e-4392-a9b5-dc84c4f469ac', 'b9752cc0-9bed-4f1c-8917-12ade7a6fdbe', 'Alice1992', '2016-07-16T19:20:30', 'available', 'Dell380', '2016-07-16T19:20:30', '2016-08-16T19:20:30', '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}', 11.5)
        self.assertEqual(o.marketplace_offer_id, "b711b1ca-a77e-4392-a9b5-dc84c4f469ac")
        self.assertEqual(o.provider_id, "b9752cc0-9bed-4f1c-8917-12ade7a6fdbe")
        self.assertEqual(o.creator_id, "Alice1992")
        self.assertEqual(o.marketplace_date_created, "2016-07-16T19:20:30")
        self.assertEqual(o.status, "available")
        self.assertEqual(o.server_id, "Dell380")
        self.assertEqual(o.start_time, "2016-07-16T19:20:30")
        self.assertEqual(o.end_time, "2016-08-16T19:20:30",)
        self.assertEqual(o.server_config,'{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}')
        self.assertEqual(o.cost, 11.5)

    def test_as_dict(self):
        '''o = OfferModel('b711b1ca-a77e-4392-a9b5-dc84c4f469ac', 'b9752ccas_dict0-9bed-4f1c-8917-12ade7a6fdbe', 'Alice1992',
                       '2016-07-16T19:20:30', 'available', 'Dell380', '2016-07-16T19:20:30', '2016-08-16T19:20:30',
                       '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
                       11.5)
        self.assertEqual(o, {
            "marketplace_offer_id": "b711b1ca-a77e-4392-a9b5-dc84c4f469ac",
            "provider_id": "b9752cc0-9bed-4f1c-8917-12ade7a6fdbe",
            "creator_id": "Alice1992",
            "marketplace_date_created": "2016-07-16T19:20:30",
            "status": "available",
            "server_id": "Dell380",
            "start_time": "2016-07-16T19:20:30",
            "end_time": "2016-08-16T19:20:30",
            "server_config": '{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.","cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
            "cost": 11.5}, "lol")'''
        pass
