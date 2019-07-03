from flocx_market.api import app
import flocx_market.conf
import flask
import unittest
from flask import jsonify

CONF = flocx_market.conf.CONF


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.app = app.create_app(app_name="test").test_client()
        self.app.testing = True
    # executed after each test

    def tearDown(self):
        pass

    def test_root_status_code(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_root_data(self):
        response = self.app.get("/", follow_redirects=True)
        flocx_market_url = CONF.api.host_ip + ":" + str(CONF.api.port)
        version = {"versions":
                   {"values": [{"status": "in progress",
                                "updated": "2019-07-02T00:00:00Z",
                                "media-types": [{"base": "application/json", "name": "flocx-market"}],
                                "links": [{"href": flocx_market_url, "rel": "self"}]}]
                    }}
        self.assertEqual(eval(response.data), version)


if __name__ == "__main__":
    unittest.main()
