import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

import broken

GOOD = {"name": "web", "port": 8080, "owner": "core"}


def test_valid_config_passes():
    assert broken.validate_config(GOOD) is True


def test_config_error_is_a_real_exception():
    assert issubclass(broken.ConfigError, Exception), "exceptions must derive from Exception"


def test_missing_key_raises_config_error():
    cfg = dict(GOOD)
    del cfg["port"]
    with pytest.raises(broken.ConfigError):
        broken.validate_config(cfg)


def test_message_names_the_missing_key():
    cfg = dict(GOOD)
    del cfg["owner"]
    with pytest.raises(broken.ConfigError) as info:
        broken.validate_config(cfg)
    assert "owner" in str(info.value), "an error message should say which key is missing"


def test_is_valid_returns_false_instead_of_raising():
    assert broken.is_valid({"name": "x"}) is False


def test_rollout_ready_filters_bad_configs():
    configs = [GOOD, {"name": "broken"}]
    assert broken.rollout_ready(configs) == ["web"]
