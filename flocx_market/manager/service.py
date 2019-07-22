from oslo_context import context as ctx
from oslo_log import log as logging
from oslo_service import service
from oslo_service import periodic_task
from oslo_service import threadgroup
import datetime

from flocx_market.objects.offer import Offer

import flocx_market.conf

CONF = flocx_market.conf.CONF
LOG = logging.getLogger(__name__)


class ManagerService(service.Service):
    def __init__(self, threads=1000):
        self.tg = threadgroup.ThreadGroup(threads)
        LOG.info("Creating flocx-market manager service")
        self.tasks = Manager(CONF)
        self._context = ctx.RequestContext(
            auth_token=None,
            project_id=None,
            is_admin=True,
            overwrite=False)

    def start(self):
        LOG.info("Starting flocx-market manager service")

        self.tg.add_dynamic_timer(
            self.tasks.run_periodic_tasks,
            initial_delay=None,
            periodic_interval_max=1,
            context=ctx
        )


class Manager(periodic_task.PeriodicTasks):

    @periodic_task.periodic_task(spacing=CONF.manager.update_expire_frequency,
                                 run_immediately=True)
    def update_expired_offers(self, context):
        LOG.info("Checking for expiring offers")
        now = datetime.datetime.utcnow()
        unexpired_offers = Offer.get_all_unexpired()
        for offer in unexpired_offers:
            if offer.end_time < now:
                offer.expire()
        if len(unexpired_offers) > 0:
            LOG.info("Updated " + str(len(unexpired_offers)) + " offers")
