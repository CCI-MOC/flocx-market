import json
from flocx_market.matcher import match_specs
from pytest import raises
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
    exp = [["inventory.system_vendor.product_name", "!startswith", "PowerEdge"]]
    assert (not match_specs(exp, data))


def test_str_end_op():
    exp = [["inventory.system_vendor.product_name", "endswith", "M620"]]
    assert (match_specs(exp, data))
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
    exp = [["root_disk.rotational", "null", "null"]]
    assert (match_specs(exp, data))
    exp = [["root_disk.test_", "null", "null"]]
    assert (not match_specs(exp, data))


def test_none_var_and_op():
    exp = [[None, "null", "null"]]
    assert (not match_specs(exp, data))
    exp = [[None, None, "null"]]
    assert (not match_specs(exp, data))
    exp = [[None, "null", None]]
    assert (not match_specs(exp, data))


def test_unknown_op():
    exp = [["cpus", "xyz", ["32", "64", "99"]]]
    assert (not match_specs(exp, data))
    exp = [["cpus", "bleh", ["64", "99"]]]
    assert (not match_specs(exp, data))


def test_invalid_data_type():
    with raises(ValueError):
        exp = [["inventory.memory.physical_mb", "<=", "755-*37"]]
        match_specs(exp, data)
        exp = [["inventory.system_vendor.product_name", "endswith", ["M620"]]]
        match_specs(exp, data)
