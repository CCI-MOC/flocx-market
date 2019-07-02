import os
from flask import Flask
from flask import Blueprint
from flask import jsonify
import flocx_market.conf
CONF = flocx_market.conf.CONF
flocx_market_api_bp = Blueprint("flocx_market_api_bp", __name__)


@flocx_market_api_bp.route('/')
def index():
    flocx_market_url = CONF.api.host_ip + ':' + str(CONF.api.port)
    version = {"versions":
               {"values": [{"status": "in progress",
                            "updated": "2019-07-02T00:00:00Z",
                            "media-types": [{"base": "application/json", "name": "flocx-market"}],
                            "links": [{"href": flocx_market_url, "rel": "self"}]}]
                }}
    return jsonify(version)


def create_app(app_name):
    app = Flask(app_name)
    app.register_blueprint(flocx_market_api_bp)
    return app
