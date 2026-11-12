import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


ENV = {
    "PAY__DB__HOST": "db.internal",
    "PAY__DB__PORT": "5432",
    "PAY__DB__POOL__MAX": "20",
    "PAY__DEBUG": "false",
    "PAY__RATIO": "0.75",
    "PAY__TLS": "True",
    "PATH": "/usr/bin",
    "LEGACY_PAY__DB__HOST": "old.internal",
}


def test_prefix_is_stripped_and_keys_lowercased():
    cfg = broken.env_to_nested(ENV)
    assert cfg["db"]["host"] == "db.internal"


def test_unrelated_and_lookalike_variables_are_ignored():
    cfg = broken.env_to_nested(ENV)
    assert set(cfg) == {"db", "debug", "ratio", "tls"}, "only names that START with the prefix count"
    assert cfg["db"]["host"] == "db.internal"


def test_integers_and_floats_are_converted():
    cfg = broken.env_to_nested(ENV)
    assert cfg["db"]["port"] == 5432 and isinstance(cfg["db"]["port"], int)
    assert cfg["ratio"] == 0.75
    assert cfg["db"]["pool"]["max"] == 20


def test_false_string_becomes_false():
    cfg = broken.env_to_nested(ENV)
    assert cfg["debug"] is False, "bool('false') is True, parse the text instead"
    assert cfg["tls"] is True


def test_siblings_in_a_section_are_all_kept():
    cfg = broken.env_to_nested(ENV)
    assert set(cfg["db"]) == {"host", "port", "pool"}


def test_custom_prefix():
    assert broken.env_to_nested({"X_A": "1", "Y_A": "2"}, prefix="X_") == {"a": 1}


def test_plain_strings_stay_strings():
    assert broken.env_to_nested({"PAY__NAME": "ledger-7"}) == {"name": "ledger-7"}


def test_describe_types_shows_python_types():
    lines = broken.describe_types({"debug": False, "db": {"port": 1}})
    assert lines == ["db:", "  port = 1 (int)", "debug = False (bool)"]
