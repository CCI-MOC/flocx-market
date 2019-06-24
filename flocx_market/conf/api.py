from oslo_config import cfg


opts = [
    cfg.HostAddressOpt('host_ip',
                       default='0.0.0.0'),
    cfg.PortOpt('port',
                default=8080),
    cfg.IntOpt('max_limit',
               default=1000),
    cfg.StrOpt('public_endpoint'),
    cfg.IntOpt('api_workers'),
    cfg.BoolOpt('enable_ssl_api',
                default=False),
]

api_group = cfg.OptGroup(
    'api',
    title='API Options')


def register_opts(conf):
    conf.register_opts(opts, group=api_group)