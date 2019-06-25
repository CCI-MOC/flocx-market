from unittest import TestCase
from flocx_market.api import app
import json


class TestOffer(TestCase):
    def test_offer(self):
        with app.test_client() as c:
            res = c.get('/offer/123')

            self.assertEqual(res.status_code, 200)
            self.assertEqual(json.loads(
                res.get_data()),
                {
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
            )
