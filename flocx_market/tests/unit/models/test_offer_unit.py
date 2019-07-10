from flocx_market.tests.unit.unit_base_test import UnitBaseTest
from flocx_market.db.sqlalchemy.offer_api import OfferApi
import datetime

now = datetime.datetime.utcnow()


class TestOfferModelUnit(UnitBaseTest):
    def test_create_offer(self):
        o = OfferApi('b9752cc0-9bed-4f1c-8917-12ade7a6fdbe', 'Alice1992', now, 'available', 'Dell380', now, now, {
            "new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server.",
            "cpu_type": "Intel Xeon", "cores": 16, "ram_gb": 512, "storage_type": "samsung SSD",
            "storage_size_gb": 204}, 11.5)
        self.assertEqual(o.provider_id, "b9752cc0-9bed-4f1c-8917-12ade7a6fdbe")
        self.assertEqual(o.creator_id, "Alice1992")
        self.assertEqual(o.marketplace_date_created, now)
        self.assertEqual(o.status, "available")
        self.assertEqual(o.server_id, "Dell380")
        self.assertEqual(o.start_time, now)
        self.assertEqual(o.end_time, now)
        self.assertEqual(o.cost, 11.5)
