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

from pytest import raises

from oslo_policy import policy as oslo_policy

from flocx_market.common import policy


def test_authorized():
    creds = {'roles': ['flocx_market_admin']}
    assert(policy.authorize('flocx_market:offer:get', creds, creds))


def test_unauthorized():
    creds = {'roles': ['generic_user']}
    with raises(oslo_policy.PolicyNotAuthorized):
        policy.authorize('flocx_market:offer:get', creds, creds)


def test_authorize_policy_not_registered():
    creds = {'roles': ['generic_user']}
    with raises(oslo_policy.PolicyNotRegistered):
        policy.authorize('flocx_market:foo:bar', creds, creds)
