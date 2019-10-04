#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import itertools

from oslo_policy import policy

import flocx_market.conf

CONF = flocx_market.conf.CONF
_ENFORCER = None

default_policies = [
    policy.RuleDefault('is_admin',
                       'role:admin or role:flocx_market_admin',
                       description='Full API access'),
]

bid_policies = [
    policy.DocumentedRuleDefault(
        'flocx_market:bid:create',
        'rule:is_admin',
        'Create bid',
        [{'path': '/bid', 'method': 'POST'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:bid:delete',
        'rule:is_admin',
        'Delete bid',
        [{'path': '/bid/{bid_ident}', 'method': 'DELETE'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:bid:get',
        'rule:is_admin',
        'Retrieve bid',
        [{'path': '/bid/{bid_ident}', 'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:bid:get_all',
        'rule:is_admin',
        'Retrieve all bids',
        [{'path': '/bid', 'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:bid:update',
        'rule:is_admin',
        'Update bid',
        [{'path': '/bid', 'method': 'PUT'}]),
]

contract_policies = [
    policy.DocumentedRuleDefault(
        'flocx_market:contract:create',
        'rule:is_admin',
        'Create contract',
        [{'path': '/contract', 'method': 'POST'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:contract:delete',
        'rule:is_admin',
        'Delete contract',
        [{'path': '/contract/{contract_ident}', 'method': 'DELETE'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:contract:get',
        'rule:is_admin',
        'Retrieve contract',
        [{'path': '/contract/{contract_ident}', 'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:contract:get_all',
        'rule:is_admin',
        'Retrieve all contracts',
        [{'path': '/contract', 'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:contract:update',
        'rule:is_admin',
        'Update contract',
        [{'path': '/contract', 'method': 'PUT'}]),
]

offer_policies = [
    policy.DocumentedRuleDefault(
        'flocx_market:offer:create',
        'rule:is_admin',
        'Create offer',
        [{'path': '/offer', 'method': 'POST'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:offer:delete',
        'rule:is_admin',
        'Delete offer',
        [{'path': '/offer/{offer_ident}', 'method': 'DELETE'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:offer:get',
        'rule:is_admin',
        'Retrieve offer',
        [{'path': '/offer/{offer_ident}', 'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:offer:get_all',
        'rule:is_admin',
        'Retrieve all offers',
        [{'path': '/offer', 'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:offer:update',
        'rule:is_admin',
        'Update offer',
        [{'path': '/offer', 'method': 'PUT'}]),
]

ocr_policies = [
    policy.DocumentedRuleDefault(
        'flocx_market:offer_contract_relationship:delete',
        'rule:is_admin',
        'Delete offer_contract_relationship',
        [{'path':
          '/offer_contract_relationship/{offer_contract_relationship_ident}',
          'method': 'DELETE'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:offer_contract_relationship:get',
        'rule:is_admin',
        'Retrieve offer_contract_relationship',
        [{'path':
          '/offer_contract_relationship/{offer_contract_relationship_ident}',
          'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:offer_contract_relationship:get_all',
        'rule:is_admin',
        'Retrieve all offer_contract_relationships',
        [{'path': '/offer_contract_relationship', 'method': 'GET'}]),
    policy.DocumentedRuleDefault(
        'flocx_market:offer_contract_relationship:update',
        'rule:is_admin',
        'Update offer_contract_relationship',
        [{'path': '/offer_contract_relationship', 'method': 'PUT'}]),
]


def list_rules():
    policies = itertools.chain(
        default_policies,
        bid_policies,
        contract_policies,
        offer_policies,
        ocr_policies,
    )
    return policies


def get_enforcer():
    CONF([], project='flocx-market')
    global _ENFORCER
    if not _ENFORCER:
        _ENFORCER = policy.Enforcer(CONF)
        _ENFORCER.register_defaults(list_rules())
    return _ENFORCER


def authorize(rule, target, creds, *args, **kwargs):
    if not CONF.api.auth_enable:
        return True

    return get_enforcer().authorize(
        rule, target, creds, do_raise=True, *args, **kwargs)
