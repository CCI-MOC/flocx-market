import os
from unittest import TestCase
from api import app
from db import db
from dotenv import load_dotenv


class TestBase(TestCase):
    def setUp(self):
        load_dotenv(".env")
        os.environ['DATABASE_URI'] = "mysql+pymysql://flocx_market:qwerty123@127.0.0.1:3307/flocx_market"
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
        with app.app_context():
            db.init_app(app)
        self.app = app.test_client()
        self.app_context = app.app_context