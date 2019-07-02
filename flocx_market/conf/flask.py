from oslo_config import cfg


opts = [
    cfg.BoolOpt('SQLALCHEMY_TRACK_MODIFICATIONS',
                default=False),
    cfg.BoolOpt('PROPAGATE_EXCEPTIONS',
                default=False)
]

flask_group = cfg.OptGroup(
    'flask',
    title='Flask Options')


def register_opts(conf):
    conf.register_opts(opts, group=flask_group)
    conf.register_cli_opts(opts, group=flask_group)
