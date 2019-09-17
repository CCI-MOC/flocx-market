from flocx_market.common import statuses
from flocx_market.matcher import matcher
from flocx_market.objects import bid
from flocx_market.objects import contract


def prepare_contract(offers_used, bid_, context):
    contract_data = dict(start_time=bid_.start_time,
                         end_time=bid_.end_time,
                         cost=bid_.cost,
                         project_id=bid_.project_id,
                         status=statuses.AVAILABLE,
                         bid_id=bid_.bid_id,
                         offers=[x.offer_id for x in offers_used]
                         )
    bid_.status = 'busy'
    bid_.save(context)
    return contract.Contract.create(contract_data, context)


def match(context):
    all_bids = bid.Bid.get_all_by_status(statuses.AVAILABLE, context)
    for b in all_bids:
        offers = matcher.\
                    get_all_matching_offers(context,
                                            b.config_query['specs'],
                                            start_time=b.start_time,
                                            end_time=b.end_time)

        if len(offers) >= b.quantity:
            offers_used = offers[:b.quantity+1]
            prepare_contract(offers_used, b, context)
