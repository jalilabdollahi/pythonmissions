import copy
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

INV = {
    "all": {"max_conns": 100, "region": "eu", "log": "info"},
    "groups": {
        "web": {"max_conns": 500, "tier": "front"},
        "canary": {"tier": "canary", "log": "debug"},
    },
    "hosts": {
        "web1": {"groups": ["web"], "vars": {}},
        "web2": {"groups": ["web"], "vars": {"max_conns": 900}},
        "web3": {"groups": ["web", "canary"], "vars": {}},
        "db1": {"groups": [], "vars": {"region": "us"}},
    },
}


def test_all_vars_are_the_floor():
    assert broken.resolve_vars(INV, "db1") == {"max_conns": 100, "region": "us", "log": "info"}


def test_group_overrides_all():
    assert broken.resolve_vars(INV, "web1")["max_conns"] == 500


def test_host_vars_override_group_vars():
    assert broken.resolve_vars(INV, "web2")["max_conns"] == 900, "host-level values have the highest precedence"


def test_later_group_overrides_earlier_group():
    r = broken.resolve_vars(INV, "web3")
    assert r["tier"] == "canary"
    assert r["log"] == "debug"
    assert r["max_conns"] == 500


def test_inventory_is_never_modified():
    snapshot = copy.deepcopy(INV)
    broken.resolve_vars(INV, "web2")
    broken.resolve_vars(INV, "web3")
    assert INV == snapshot, "resolving a host must not change the inventory"


def test_resolution_order_does_not_matter():
    first = broken.resolve_vars(INV, "web3")
    broken.resolve_vars(INV, "db1")
    assert broken.resolve_vars(INV, "web3") == first
    assert "tier" not in broken.resolve_vars(INV, "db1")


def test_unknown_host_and_group():
    with pytest.raises(KeyError):
        broken.resolve_vars(INV, "ghost")
    bad = {"all": {}, "groups": {}, "hosts": {"h": {"groups": ["nope"], "vars": {}}}}
    with pytest.raises(KeyError):
        broken.resolve_vars(bad, "h")


def test_diff_hosts():
    assert broken.diff_hosts(INV, "web1", "web2") == {"max_conns": (500, 900)}
