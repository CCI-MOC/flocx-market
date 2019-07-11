from flask import Flask
from flask_restful import Api
from flocx_market.api.offer import Offer
from flocx_market.api.root import Root
import flocx_market.conf


CONF = flocx_market.conf.CONF


def create_app(app_name):
    app = Flask(app_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = CONF.database.connection
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = (
        CONF.flask.SQLALCHEMY_TRACK_MODIFICATIONS
    )
    app.config['PROPAGATE_EXCEPTIONS'] = CONF.flask.PROPAGATE_EXCEPTIONS
    api = Api(app)
    api.add_resource(Offer,
                     '/offer',
                     '/offer/',
                     '/offer/<string:marketplace_offer_id>')
    api.add_resource(Root, '/')
    return app
