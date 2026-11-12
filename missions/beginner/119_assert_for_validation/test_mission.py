import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import validate_replicas, validate_environment, build_manifest


def test_valid_replicas_are_returned():
    assert validate_replicas(3) == 3
    assert validate_replicas(50) == 50


def test_replicas_above_limit_raise_value_error():
    with pytest.raises(ValueError):
        validate_replicas(100000)


def test_zero_and_negative_replicas_raise_value_error():
    for bad in (0, -4):
        with pytest.raises(ValueError):
            validate_replicas(bad)


def test_non_integer_replicas_raise_value_error():
    for bad in ("3", 2.5, True, None):
        with pytest.raises(ValueError):
            validate_replicas(bad)


def test_unknown_environment_raises_value_error():
    with pytest.raises(ValueError, match="unknown environment"):
        validate_environment("qa")


def test_known_environments_are_accepted():
    assert [validate_environment(e) for e in ("dev", "staging", "prod")] == ["dev", "staging", "prod"]


def test_build_manifest():
    assert build_manifest("billing", 3, "prod") == {"service": "billing", "replicas": 3, "environment": "prod"}
    with pytest.raises(ValueError):
        build_manifest("billing", 0, "prod")
