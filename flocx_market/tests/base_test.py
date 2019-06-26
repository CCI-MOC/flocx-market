from unittest import TestCase
from flocx_market.api import app
from flocx_market.db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # ensure db exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gpdwpyrw:UCzgXashsqnX99ASMK2SxZK8d4tbEUa6@raja.db.elephantsql.com:5432/gpdwpyrw'
        # use instance of app for following code block
        with app.app_context():
            #initilaize SQLalchemy instance with our app
            db.init_app(app)

    def setUp(self):
        #ensure db exists
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gpdwpyrw:UCzgXashsqnX99ASMK2SxZK8d4tbEUa6@raja.db.elephantsql.com:5432/gpdwpyrw'
        #use instance of app for following code block
        with app.app_context():
            #create tables
            db.create_all()
        #create a new test client of the app
        self.app = app.test_client
        '''allow us to access app context later on in our tests, which
        will load up everything that is relevant to the app so we can create a context manager
        and access the db, etc.'''
        self.app_context = app.app_context

    def tearDown(self):
        #ensure db is deleted
        with app.app_context():
            #rm everythign from current session
            db.session.remove()
            #drop all tables form db
            db.drop_all()