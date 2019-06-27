import os
from flask import Flask
from flask import Blueprint
from flask_keystone import FlaskKeystone
from flask_oslolog import OsloLog
from oslo_config import cfg


key = FlaskKeystone()
log = OsloLog()

my_bp = Blueprint("my_bp", __name__)


@my_bp.route('/')
def index():
    conf = cfg.CONF
    print(conf.database.connection)
    return "Hello World"

def create_app(app_name):
    app = Flask(app_name)
    # log.init_app(app)
    # key.init_app(app)
    app.register_blueprint(my_bp)
    return app
