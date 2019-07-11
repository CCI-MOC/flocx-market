import jmespath
import re
from flocx_market.db.sqlalchemy.offer_api import OfferApi


def apply_operator(val1, val2, op):

    # null operator
    if op is None and val1 is not None:
        return val1

    neg = False
    ret_val = False

    if op.startswith('!'):
        neg = True
        op = op[1:]
        if op == '=':
            op = '=='

    all_num_ops = ['==', '<', '<=', '>', '>=']
    all_str_ops = ['eq', 'ne', 'startswith', 'endswith', 'matches']
    all_list_ops = ['in', 'contains']

    # all numeric operations
    if op in all_num_ops:

        val1 = float(val1)
        val2 = float(val2)

        if op == '==':
            ret_val = val1 == val2

        if op == '>':
            ret_val = val1 > val2

        if op == '>=':
            ret_val = val1 >= val2

        if op == '<':
            ret_val = val1 < val2

        if op == '<=':
            ret_val = val1 <= val2

    # string operations
    elif op in all_str_ops:
        val1 = str(val1)
        val2 = str(val2)

        if op == 'eq':
            ret_val = val1 == val2

        if op == 'ne':
            ret_val = val1 != val2

        if op == 'startswith':
            ret_val = val1.startswith(val2)

        if op == 'endswith':
            ret_val = val1.endswith(val2)

        if op == 'matches':
            if re.search(val2, val1):
                ret_val = True
            else:
                ret_val = False

    # list operators
    elif op in all_list_ops:

        if op == 'in':
            val1 = val1
            val2 = list(val2)
            ret_val = val1 in val2

        if op == 'contains':
            val1 = list(val1)
            val2 = val2
            ret_val = val2 in val1
    else:
        raise ValueError

    if neg:
        return not ret_val
    else:
        return ret_val


def match_specs(match_expression, data):
    for exp in match_expression:

        j_val = jmespath.search(exp[0], data)
        op = exp[1]
        val = exp[2]

        if not apply_operator(j_val, val, op):
            return False

    return True


def get_all_offers_matching_specs(specs):

    all_offers = OfferApi.query.all()
    matching_offers = []

    for offer in all_offers:
        if match_specs(specs, offer.server_config):
            matching_offers.append(offer)

    return matching_offers
