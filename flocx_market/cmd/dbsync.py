from flocx_market.cmd import api
from flocx_market.db.orm import orm


def main():
    application = api.create_app()
    orm.init_app(application)
    orm.create_all()
