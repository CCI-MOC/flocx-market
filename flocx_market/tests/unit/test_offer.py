from unittest import TestCase
from flocx_market.models.offer import OfferModel


class TestOfferModel(TestCase):

    def test_create_offer(self):
        o = OfferModel("123", "123", "123", "01-01-2019", "active", "123", "time", "time", "json", 13.5)
        self.assertEqual("123", o.marketplace_offer_id)
        self.assertEqual("123", o.provider_id)
        self.assertEqual("123", o.creator_id)
        self.assertEqual("01-01-2019", o.marketplace_date_created)
        self.assertEqual("active", o.status)
        self.assertEqual("123", o.server_id)
        self.assertEqual("time", o.start_time)
        self.assertEqual("time", o.end_time)
        self.assertEqual("json", o.server_config)
        self.assertEqual(13.5, o.cost)

    def test_json(self):
        o = OfferModel("123", "123", "123", "01-01-2019", "active", "123", "time", "time", "json", 13.5)
        expected = {
            'marketplace_offer_id': '123',
            'provider_id': '123',
            'creator_id': '123',
            'marketplace_date_created': '01-01-2019',
            'status': 'active',
            'server_id': '123',
            'start_time': 'time',
            'end_time': 'time',
            'server_config': 'json',
            'cost': '13.5'}

        self.assertDictEqual(expected, o.json())

    def test_find_by_id(self):
        pass

    def test_save_to_db(self):
        pass

    def test_delete_from_db(self):
        pass
