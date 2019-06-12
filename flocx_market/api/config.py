
# Pecan Application Configurations
app = {
    'root': 'flocx_market.api.controllers.root.RootController',
    'modules': ['flocx_market.api'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/flocx_market/templates',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
}
