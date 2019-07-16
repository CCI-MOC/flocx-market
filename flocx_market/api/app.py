from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flocx_market.api.offer import Offer
from flocx_market.api.root import Root
from flocx_market.api.bid import Bid
from flocx_market.db.orm import orm
import flocx_market.conf

from keystonemiddleware import auth_token

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
    api.add_resource(Bid,
                     '/bid',
                     '/bid/',
                     '/bid/<string:marketplace_bid_id>')
    api.add_resource(Root, '/')

    Migrate(app, orm)
    orm.init_app(app)

    if CONF.api.auth_enable:
        app = auth_token.AuthProtocol(app, dict(CONF.keystone_authtoken))

    return app
