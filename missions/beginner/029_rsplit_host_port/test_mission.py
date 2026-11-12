import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import parse_endpoint, replica_map


def test_plain_host_and_port():
    assert parse_endpoint("db1.internal:5433") == ("db1.internal", 5433)


def test_port_is_an_int():
    assert isinstance(parse_endpoint("db1:6000")[1], int)


def test_bare_host_uses_default_port():
    assert parse_endpoint("db2") == ("db2", 5432)
    assert parse_endpoint("db2", default_port=6432) == ("db2", 6432)


def test_ipv6_with_port_splits_on_last_colon():
    assert parse_endpoint("[::1]:5433") == ("::1", 5433), "only the final colon separates the port"


def test_ipv6_brackets_are_removed_from_host():
    host, _ = parse_endpoint("[2001:db8::7]:5500")
    assert host == "2001:db8::7", "the host must not keep its brackets"


def test_replica_map_handles_mixed_formats():
    assert replica_map(["a:1", "b", " [::1]:7 "]) == {"a": 1, "b": 5432, "::1": 7}
