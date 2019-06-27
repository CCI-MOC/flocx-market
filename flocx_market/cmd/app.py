from flocx_market.api import app
from flocx_market.db.orm import orm
from flask_migrate import Migrate

application = app.create_app(app_name='flocx-market')
migrate = Migrate(application, orm)

if __name__ == '__main__':

    orm.init_app(application)
    application.run(port=8080, debug=True)
