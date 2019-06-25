import jmespath
import re


def apply_operator(val1, val2, op):

    if val1 is None or val2 is None or op is None:
        return False

    # null operator
    if op == 'null':
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
    if op in all_str_ops:
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
    if op in all_list_ops:

        if op == 'in':
            val1 = val1
            val2 = list(val2)
            ret_val = val1 in val2

        if op == 'contains':
            val1 = list(val1)
            val2 = val2
            ret_val = val2 in val1

    if neg:
        return not ret_val
    else:
        return ret_val


def match_specs(match_expression, data):
    for exp in match_expression:
        if None in exp:
            return False

        j_val = jmespath.search(exp[0], data)
        op = exp[1]
        val = exp[2]
        if not apply_operator(j_val, val, op):
            return False
    return True
