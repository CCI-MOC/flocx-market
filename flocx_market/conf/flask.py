from oslo_config import cfg


opts = [
    cfg.StrOpt('SQLALCHEMY_DATABASE_URI',
               default='mysql+pymysql://flocx_market:qwerty123@127.0.0.1:3306/flocx_market'),
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