import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import DEFAULT_ALLOWED, build_config, allowed_count


def test_defaults_are_included():
    cfg = build_config("globex")
    assert cfg["allowed"] == ["10.0.0.0/8", "192.168.0.0/16"]


def test_extra_ranges_are_appended():
    cfg = build_config("acme", ["172.16.0.0/12"])
    assert cfg["allowed"] == ["10.0.0.0/8", "192.168.0.0/16", "172.16.0.0/12"]


def test_default_list_is_never_modified():
    build_config("acme", ["172.16.0.0/12"])
    assert DEFAULT_ALLOWED == ["10.0.0.0/8", "192.168.0.0/16"], "the shared default must stay untouched"


def test_customers_do_not_see_each_others_ranges():
    build_config("acme", ["172.16.0.0/12"])
    other = build_config("globex")
    assert "172.16.0.0/12" not in other["allowed"]


def test_configs_do_not_share_a_list():
    a = build_config("a")
    b = build_config("b")
    assert a["allowed"] is not b["allowed"]
    assert allowed_count(a) == 2
