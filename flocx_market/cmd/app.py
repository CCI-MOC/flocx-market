from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from resources.offer import Offer, OfferList

app = Flask(__name__)
api = API(app)

api.add_resource(Offer, '/offer/<string:id>')
api.add_resource(OfferList, '/offers')

if __name__ == '__main__':
    app.run(debug = True)
