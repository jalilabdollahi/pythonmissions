import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import plan, resolve_canary_percent, resolve_replicas


def test_requested_value_is_used():
    assert resolve_replicas(5) == 5


def test_none_uses_default():
    assert resolve_replicas(None) == 2
    assert resolve_replicas(None, default=3) == 3


def test_zero_replicas_is_respected():
    assert resolve_replicas(0) == 0, "0 replicas is a real request, not a missing value"


def test_canary_defaults_to_ten():
    assert resolve_canary_percent({}) == 10
    assert resolve_canary_percent({"canary_percent": None}) == 10


def test_zero_percent_canary_is_respected():
    assert resolve_canary_percent({"canary_percent": 0}) == 0


def test_plan_keeps_scaled_to_zero_apps_off():
    apps = {"preview-a": {"replicas": 0}, "preview-b": {}, "preview-c": {"replicas": 4}}
    assert plan(apps) == {"preview-a": 0, "preview-b": 2, "preview-c": 4}
