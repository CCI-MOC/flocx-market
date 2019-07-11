import json

import flocx_market.conf

CONF = flocx_market.conf.CONF


def test_root_status_code(client):
    response = client.get("/", follow_redirects=True)
    assert response.status_code == 200


def test_root_data(client):
    response = client.get("/", follow_redirects=True)
    flocx_market_url = CONF.api.host_ip + ":" + str(CONF.api.port)
    version = {
        "versions": {
            "values": [{
                "status":
                "in progress",
                "updated":
                "2019-07-02T00:00:00Z",
                "media-types": [{
                    "base": "application/json",
                    "name": "flocx-market"
                }],
                "links": [{
                    "href": flocx_market_url,
                    "rel": "self"
                }]
            }]
        }
    }
    assert json.loads(response.data) == version
