import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flocx_market.db import models as db_models


_ENGINE = None
_SESSION_MAKER = None

#1.connecting
def get_engine():
    global _ENGINE
    if _ENGINE is not None:
        return _ENGINE

    _ENGINE = create_engine('mysql+pymysql://flocx_market:qwerty123@127.0.0.1:3306/flocx_market', echo=True)
    # db_models.Base.metadata.create_all(_ENGINE)
    return _ENGINE

#2.creating a session
def get_session_maker(engine):
    global _SESSION_MAKER
    if _SESSION_MAKER is not None:
        return _SESSION_MAKER

    _SESSION_MAKER = sessionmaker(bind=engine)
    return _SESSION_MAKER

def get_session():
    engine = get_engine()
    Session = get_session_maker(engine)
    session = Session()

    return session

#3.adding and updating object
class Connection(object):

    def __init__(self):
        pass

    def get_offer(self, id):
        query = get_session().query(db_models.Offer).filter_by(id=id)
        try:
            offer = query.one()
        except exc.NoResultFound:
            # TODO(developer): process this situation
            pass

        return offer

    def list_offers(self):
        session = get_session()
        query = session.query(db_models.Offer)
        offers = query.all()

        return offers

    def update_offer(self, offer):
        pass

    def delete_offer(self, offer):
        pass