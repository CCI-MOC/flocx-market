import os

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from flocx_market.api.offer import Offer, OfferList
from flocx_market.api.bid import Bid, BidList
from flocx_market.api.contract import Contract, ContractList


def create_app(app_name):

    app = Flask(app_name)
    load_dotenv(".env")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    api = Api(app)
    api.add_resource(Offer, '/offer', '/offers/<string:marketplace_offer_id>')
    api.add_resource(OfferList, '/offers')
    api.add_resource(Bid, '/bid', '/bids/<string:marketplace_bid_id>')
    api.add_resource(BidList, '/bids')
    api.add_resource(Contract, '/contract', '/contracts/<string:contract_id>')
    api.add_resource(ContractList, '/contracts')
    return app
