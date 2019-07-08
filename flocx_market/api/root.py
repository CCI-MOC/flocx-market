from flask import jsonify
from flask_restful import Resource
import flocx_market.conf

CONF = flocx_market.conf.CONF


class Root(Resource):
    @classmethod
    def get(cls):
        flocx_market_url = CONF.api.host_ip + ':' + str(CONF.api.port)
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
        return jsonify(version)
