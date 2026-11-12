import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import by_port, owner_of, free_ports, check_config


def test_by_port_inverts_a_clean_mapping():
    assert by_port({"api": 8080, "web": 8081}) == {8080: "api", 8081: "web"}


def test_duplicate_port_raises_value_error():
    with pytest.raises(ValueError):
        by_port({"api": 8080, "web": 8081, "metrics": 8080})


def test_error_message_names_port_and_both_services():
    with pytest.raises(ValueError) as info:
        by_port({"api": 8080, "metrics": 8080})
    msg = str(info.value)
    assert "8080" in msg and "api" in msg and "metrics" in msg, "say which services clash"


def test_empty_config_is_fine():
    assert by_port({}) == {}


def test_owner_of_known_and_unknown_port():
    cfg = {"api": 8080}
    assert owner_of(cfg, 8080) == "api"
    assert owner_of(cfg, 9) is None


def test_free_ports_keeps_candidate_order():
    assert free_ports({"api": 8080}, [8082, 8080, 8081]) == [8082, 8081]


def test_check_config_reports_conflict():
    assert check_config({"a": 1, "b": 2}) == "ok"
    assert check_config({"a": 1, "b": 1}) == "conflict: port 1 used by a and b"
