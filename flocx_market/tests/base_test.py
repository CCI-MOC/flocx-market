from unittest import TestCase
from flocx_market.cmd.app import application
from flocx_market.db.orm import orm


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # ensure db exists
        application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gpdwpyrw:UCzgXashsqnX99ASMK2SxZK8d4tbEUa6@raja.db.elephantsql.com:5432/gpdwpyrw'
        # use instance of app for following code block
        with application.app_context():
            # initilaize SQLalchemy instance with our app
            orm.init_app(application)

    def setUp(self):
        # ensure db exists
        application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gpdwpyrw:UCzgXashsqnX99ASMK2SxZK8d4tbEUa6@raja.db.elephantsql.com:5432/gpdwpyrw'
        # use instance of app for following code block
        with application.app_context():
            # create tables
            orm.create_all()
        # create a new test client of the app
        self.app = application.test_client
        '''allow us to access app context later on in our tests, which
        will load up everything that is relevant to the app so we can create a context manager
        and access the db, etc.'''
        self.app_context = application.app_context

    def tearDown(self):
        # ensure db is deleted
        with application.app_context():
            # rm everythign from current session
            orm.session.remove()
            # drop all tables form db
            orm.drop_all()
