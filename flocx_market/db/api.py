import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flocx_market.db import models as db_models
from sqlalchemy.sql import text

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
    create_sample_data(engine)
    return session

def create_sample_data(engine):
    con = engine.connect()
    data =  { "id":1,\
        "marketplace_offer_id":"b711b1ca-a77e-4392-a9b5-dc84c4f469ac",\
        "provider_id":"b9752cc0-9bed-4f1c-8917-12ade7a6fdbe",\
        "creator_id":"Alice1992",\
        "marketplace_date_created":"2016-07-16T19:20:30",\
        "status":"available",\
        "server_name:":"Dell380",\
        "start_time":"2016-07-16T19:20:30",\
        "end_time": "2016-08-16T19:20:30",\
        "duration":164,\
        "server_config":'{"new attribute XYZ": "This is just a sample list of free-form attributes used for describing a server."\
        ,"cpu_type": "Intel Xeon","cores": 16,"ram_gb": 512,"storage_type": "samsung SSD", "storage_size_gb": 204}',
        "cost":11 }
    con.execute("DELETE FROM offer WHERE id = 1")
    statement = text("""INSERT INTO offer VALUES(:id, :marketplace_offer_id, :provider_id, :creator_id, \
        :marketplace_date_created, :status, "Dell380", :start_time, :end_time, :duration, :server_config, :cost)""")
    con.execute(statement, **data)
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