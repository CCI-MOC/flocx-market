import sys

from flocx_market.api import app
from flocx_market.common import service as flocx_market_service
from flocx_market.db.orm import orm


def main():
    flocx_market_service.prepare_service(sys.argv)
    application = app.create_app("dbsync")
    with application.app_context():
        orm.init_app(application)
        orm.create_all()
