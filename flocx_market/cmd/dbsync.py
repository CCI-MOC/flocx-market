import sys

from flocx_market.common import service as flocx_market_service
from flocx_market.db.sqlalchemy import api as db_api


def main():
    flocx_market_service.prepare_service(sys.argv)
    db_api.setup_db()
