import datetime
import json
from pytest import raises
import unittest.mock as mock

from oslo_context import context as ctx

from flocx_market.common import statuses
from flocx_market.matcher.matcher import match_specs
from flocx_market.matcher.matcher import get_all_matching_offers
from flocx_market.objects import offer
from flocx_market.resource_objects import resource_types

now = datetime.datetime.utcnow()

scoped_context = ctx.RequestContext(is_admin=False,
                                    project_id='5599')

data = json.loads(""" {
    "name": "abc_def",
    "cpu_arch": "x86_64",
    "root_disk": {
    "rotational": true,
    "test_": false
    },
    "interface": ["eth0", "lo0", "eth1"],
    "cpus": 32,
    "inventory": {
    "boot": {
        "current_boot_mode": "bios"
        },
    "system_vendor": {
        "product_name": "PowerEdge M620"
        },
    "memory": {
        "physical_mb": 65536
        }
    }
}""")


def test_num_eq_op():
    exp = [["inventory.memory.physical_mb", "==", 65536]]
    assert (match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "==", 65537]]
    assert (not match_specs(exp, data))


def test_num_not_eq_op():
    exp = [["inventory.memory.physical_mb", "!=", 65536]]
    assert (not match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "!=", 65537]]
    assert (match_specs(exp, data))


def test_num_greater_op():
    exp = [["inventory.memory.physical_mb", ">", 55536]]
    assert (match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "!>", 55536]]
    assert (not match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", ">", 75537]]
    assert (not match_specs(exp, data))


def test_num_greater_eq_op():
    exp = [["inventory.memory.physical_mb", ">=", 55536]]
    assert (match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", ">=", 65536]]
    assert (match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", ">=", 75537]]
    assert (not match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "!>=", 75537]]
    assert (match_specs(exp, data))


def test_num_lesser_op():
    exp = [["inventory.memory.physical_mb", "<", 75537]]
    assert (match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "!<", 75537]]
    assert (not match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "<", 55537]]
    assert (not match_specs(exp, data))


def test_num_lesser_eq_op():
    exp = [["inventory.memory.physical_mb", "<=", 75537]]
    assert (match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "<=", 65536]]
    assert (match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "<=", 45537]]
    assert (not match_specs(exp, data))
    exp = [["inventory.memory.physical_mb", "!<=", 45537]]
    assert (match_specs(exp, data))


def test_str_eq_op():
    exp = [["inventory.boot.current_boot_mode", "eq", "bios"]]
    assert (match_specs(exp, data))
    exp = [["inventory.boot.current_boot_mode", "eq", "test"]]
    assert (not match_specs(exp, data))
    exp = [["inventory.boot.current_boot_mode", "!eq", "test"]]
    assert (match_specs(exp, data))


def test_str_not_eq_op():

    exp = [["inventory.boot.current_boot_mode", "ne", "bios"]]
    assert (not match_specs(exp, data))
    exp = [["inventory.boot.current_boot_mode", "ne", "test"]]
    assert (match_specs(exp, data))
    exp = [["inventory.boot.current_boot_mode", "!ne", "test"]]
    assert (not match_specs(exp, data))


def test_str_start_op():
    exp = [["inventory.system_vendor.product_name", "startswith", "M620"]]
    assert (not match_specs(exp, data))
    exp = [["inventory.system_vendor.product_name", "startswith", "PowerEdge"]]
    assert (match_specs(exp, data))
    exp = [["inventory.system_vendor.product_name",
            "!startswith",
            "PowerEdge"]]
    assert (not match_specs(exp, data))


def test_str_end_op():
    exp = [["inventory.system_vendor.product_name", "endswith", "M620"]]
    assert (match_specs(exp, data))
    exp = [["inventory.system_vendor.product_name", "endswith", ["M620"]]]
    assert (not match_specs(exp, data))
    exp = [["inventory.system_vendor.product_name", "endswith", "PowerEdge"]]
    assert (not match_specs(exp, data))
    exp = [["inventory.system_vendor.product_name", "!endswith", "PowerEdge"]]
    assert (match_specs(exp, data))


def test_str_match_op():
    exp = [["name", "matches", "[a-m]"]]
    assert (match_specs(exp, data))
    exp = [["name", "matches", "[n-z]"]]
    assert (not match_specs(exp, data))
    exp = [["name", "!matches", "[n-z]"]]
    assert (match_specs(exp, data))


def test_list_contains_op():
    exp = [["interface", "contains", "eth0"]]
    assert (match_specs(exp, data))
    exp = [["interface", "contains", "xyz"]]
    assert (not match_specs(exp, data))
    exp = [["interface", "!contains", "xyz"]]
    assert (match_specs(exp, data))


def test_list_in_op():
    exp = [["cpus", "in", [32, 64, 99]]]
    assert (match_specs(exp, data))
    exp = [["cpus", "in", [64, 99]]]
    assert (not match_specs(exp, data))
    exp = [["cpus", "!in", [64, 99]]]
    assert (match_specs(exp, data))


def test_none_op():
    exp = [["root_disk.rotational", None, "null"]]
    assert (match_specs(exp, data))
    exp = [["root_disk.test_", None, "null"]]
    assert (not match_specs(exp, data))


def test_unknown_op():
    with raises(ValueError):
        exp = [["cpus", "xyz", ["32", "64", "99"]]]
        match_specs(exp, data)
    with raises(ValueError):
        exp = [["cpus", "bleh", ["64", "99"]]]
        match_specs(exp, data)


def test_invalid_data_type():
    with raises(ValueError):
        exp = [["inventory.memory.physical_mb", "<=", "755-*37"]]
        match_specs(exp, data)


test_offer_1 = dict(
        offer_id='test_offer_1',
        creator_id='3456',
        date_created=now,
        status=statuses.AVAILABLE,
        resource_id='4567',
        resource_type=resource_types.IRONIC_NODE,
        start_time=now,
        end_time=now,
        config={'memory': 204},
        cost=0.0,
        contract_id=None,
        project_id='5599'
        )

test_offer_2 = dict(
        offer_id='test_offer_2',
        creator_id='3456',
        date_created=now,
        status=statuses.AVAILABLE,
        resource_id='457',
        resource_type=resource_types.IRONIC_NODE,
        start_time=now,
        end_time=now,
        config={'memory': 203},
        cost=0.0,
        contract_id=None,
        project_id='5599'
        )


def test_0_match(app, db, session):
    assert len(get_all_matching_offers(
        scoped_context,
        [["memory", "==", 204]])) == 0


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.is_resource_admin')
def test_1_match(is_resource_admin, app, db, session):
    is_resource_admin.return_vale = True
    offer.Offer.create(test_offer_1, scoped_context)
    assert len(get_all_matching_offers(
        scoped_context,
        [["memory", "==", 204]])) == 1


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.is_resource_admin')
def test_only_1_match(is_resource_admin, app, db, session):
    is_resource_admin.return_vale = True
    offer.Offer.create(test_offer_1, scoped_context)
    offer.Offer.create(test_offer_2, scoped_context)
    assert len(get_all_matching_offers(
        scoped_context,
        [["memory", "==", 203]])) == 1


@mock.patch('flocx_market.resource_objects.ironic_node'
            '.IronicNode.is_resource_admin')
def test_2_match(is_resource_admin, app, db, session):
    is_resource_admin.return_vale = True
    offer.Offer.create(test_offer_1, scoped_context)
    offer.Offer.create(test_offer_2, scoped_context)
    assert len(get_all_matching_offers(
        scoped_context,
        [["memory", ">", 202]])) == 2
