from flask import Flask, request
from flask_restful import Api

from resources.offer import Offer, OfferList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flocx_market:qwerty123@127.0.0.1:3306/flocx_market'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = API(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(Offer, '/offer/<string:marketplace_offer_id>')
api.add_resource(OfferList, '/offers')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug = True)
