import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

GOOD = {"name": "api", "port": 8080, "replicas": 2, "env": {"A": "1"}}


def test_valid_manifest_has_no_errors():
    assert broken.validate_manifest(GOOD) == []


def test_all_errors_reported_in_one_run():
    errors = broken.validate_manifest({"name": "", "port": 70000, "replicas": 0, "env": []})
    assert len(errors) == 4, "collect every error instead of stopping at the first"
    assert errors[0].startswith("name")
    assert errors[1].startswith("port")
    assert errors[2].startswith("replicas")
    assert errors[3].startswith("env")


def test_missing_keys_each_reported():
    errors = broken.validate_manifest({})
    assert errors == [
        "name is missing",
        "port is missing",
        "replicas is missing",
        "env is missing",
    ]


def test_zero_replicas_is_invalid_not_missing():
    errors = broken.validate_manifest({**GOOD, "replicas": 0})
    assert errors == ["replicas must be an integer >= 1"]


def test_empty_env_dict_is_valid():
    assert broken.validate_manifest({**GOOD, "env": {}}) == []


def test_boolean_is_not_an_integer():
    errors = broken.validate_manifest({**GOOD, "replicas": True})
    assert errors == ["replicas must be an integer >= 1"]
    errors = broken.validate_manifest({**GOOD, "port": True})
    assert len(errors) == 1


def test_assert_valid_joins_messages():
    with pytest.raises(ValueError) as info:
        broken.assert_valid({**GOOD, "port": 0, "name": " "})
    message = str(info.value)
    assert "name must" in message and "port must" in message
    broken.assert_valid(GOOD)
