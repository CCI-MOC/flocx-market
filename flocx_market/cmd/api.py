import os

from flask import Flask, request
from flask_restful import Api

from flocx_market.resources.offer import Offer, OfferList
from oslo_context import context


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', CONF)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

api.add_resource(Offer, '/offer', '/offer/<string:marketplace_offer_id>')
api.add_resource(OfferList, '/offers')


if __name__ == '__main__':
    from flocx_market.models.db import db
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        db.create_all()

    app.run(port=8080, debug=True)
