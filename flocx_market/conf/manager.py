from oslo_config import cfg


opts = [
    cfg.IntOpt('update_expire_frequency',
               default=60,
               help="The frequency in which the manager's periodic task will run.\
                    Enter in seconds")
]

manager_group = cfg.OptGroup(
    'manager',
    title='Manager Options')


def register_opts(conf):
    conf.register_opts(opts, group=manager_group)
    conf.register_cli_opts(opts, group=manager_group)
