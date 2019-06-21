import os

from flask import Flask, request
from flask_restful import Api
from flask_migrate import Migrate
import pymysql
from dotenv import load_dotenv
from db import db

from resources.offer import Offer, OfferList

app = Flask(__name__)
load_dotenv(".env")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
migrate = Migrate(app, db)
api.add_resource(Offer, '/offer', '/offer/<string:marketplace_offer_id>')
api.add_resource(OfferList, '/offers')

if __name__ == '__main__':
    db.init_app(app)

    app.run(port=8080, debug=True)
