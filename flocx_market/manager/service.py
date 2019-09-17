from oslo_context import context as ctx
from oslo_log import log as logging
from oslo_service import service
from oslo_service import periodic_task
from oslo_service import threadgroup
import datetime

from flocx_market.common import statuses
from flocx_market.matcher import match_engine
from flocx_market.objects.offer import Offer
from flocx_market.objects.bid import Bid
from flocx_market.objects.contract import Contract
from flocx_market.objects.offer_contract_relationship import \
    OfferContractRelationship
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
            context=self._context
        )


class Manager(periodic_task.PeriodicTasks):

    @periodic_task.periodic_task(spacing=CONF.manager.update_expire_frequency,
                                 run_immediately=True)
    def update_expired_offers(self, context):
        LOG.info("Checking for expiring offers")
        now = datetime.datetime.utcnow()
        unexpired_offers = Offer.get_all_unexpired(context)
        exp = 0
        for offer in unexpired_offers:
            if offer.end_time < now:
                offer.expire(context)
                offer_id = offer.offer_id
                filters = {'offer_id': offer_id}
                unexpired_ocrs = OfferContractRelationship.get_all(context,
                                                                   filters)
                for ocr in unexpired_ocrs:
                    ocr.expire(context)
                exp += 1
        if exp > 0:
            LOG.info("Updated " + str(exp) + " offers")

    @periodic_task.periodic_task(spacing=CONF.manager.update_expire_frequency,
                                 run_immediately=True)
    def update_expired_bids(self, context):
        LOG.info("Checking for expiring offers")
        now = datetime.datetime.utcnow()
        unexpired_bids = Bid.get_all_unexpired(context)
        exp = 0
        for bid in unexpired_bids:
            if bid.end_time < now:
                bid.expire(context)
                exp += 1
        if exp > 0:
            LOG.info("Updated " + str(exp) + " bids")

    @periodic_task.periodic_task(spacing=CONF.manager.update_expire_frequency,
                                 run_immediately=True)
    def update_contracts(self, context):
        LOG.info("Checking for expiring contracts")
        now = datetime.datetime.utcnow()

        unexpired_contracts = Contract.get_all_unexpired(context)
        for contract in unexpired_contracts:
            if contract.end_time < now:
                contract.expire(context)
                LOG.info("Expiring contract " + contract.contract_id)

        LOG.info("Checking for contracts to fulfill")
        contracts_to_fulfill = Contract.get_all_by_status(
            context, statuses.AVAILABLE)
        for contract in contracts_to_fulfill:
            if contract.start_time >= now:
                contract.fulfill(context)
                LOG.info("Fulfilled contract " + contract.contract_id)

    @periodic_task.periodic_task(spacing=CONF.manager.matcher_frequency,
                                 run_immediately=True)
    def matcher(self, context):
        LOG.info("Matching bids and offers")
        match_engine.match(context)
