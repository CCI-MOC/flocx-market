import pecan
from pecan import make_app
from flocx_market.api import config as api_config
from flocx_market.api import hooks

def get_pecan_config():
    filename = api_config.__file__.replace('.pyc', '.py')   # get the absolute path of the pecan config.py
    return pecan.configuration.conf_from_file(filename)

def setup_app():
    config = get_pecan_config()
    app_hooks = [hooks.DBHook()]
    app_conf = dict(config.app)
    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks=app_hooks,
        **app_conf)
    return app

