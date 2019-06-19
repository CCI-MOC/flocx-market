import pecan
from oslo_context import context
from pecan import hooks
import flocx_market.conf

CONF = flocx_market.conf.CONF

class ContextHook(hooks.PecanHook):
    def before(self, state):
        ctx = context.RequestContext.from_environ(state.request.environ)
        state.request.context = ctx

    def after(self, state):
        state.request.context = None

def get_pecan_config():
    cfg_dict = {
        "app": {
            "root": CONF.pecan.root,
            "modules": CONF.pecan.modules,
            "debug": CONF.pecan.debug,
            "auth_enable": CONF.pecan.auth_enable
        }
    }

    return pecan.configuration.conf_from_dict(cfg_dict)

def setup_app(config=None):
    if not config:
        config = get_pecan_config()

    pecan.configuration.set_config(dict(config), overwrite=True)

    app = pecan.make_app(
        config.app.root,
        hooks=lambda: [ContextHook()],
        debug=CONF.pecan.debug,
        static_root=config.app.static_root if CONF.pecan.debug else None,
        force_canonical=getattr(config.app, 'force_canonical', True),
    )
    # keystone authentication:
    # if CONF.pecan.auth_enable:
    #     app = auth_token.AuthProtocol(app, dict(CONF.keystone_authtoken))

    return app

