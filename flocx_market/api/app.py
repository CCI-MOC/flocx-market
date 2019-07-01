from flask import Flask
from flask_restful import Api
from flocx_market.api.offer import Offer
from flask import Blueprint
from flask import jsonify
import flocx_market.conf
from oslo_config import cfg


CONF = flocx_market.conf.CONF


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
    app.config['SQLALCHEMY_DATABASE_URI'] = CONF.database.connection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONF.flask.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['PROPAGATE_EXCEPTIONS'] = CONF.flask.PROPAGATE_EXCEPTIONS
    app.route('/')(index)
    api = Api(app)
    api.add_resource(Offer, '/offer', '/offers/<string:marketplace_offer_id>')
    return app
