import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_millicore_suffix_is_already_thousandths():
    assert broken.parse_cpu("250m") == 250
    assert broken.parse_cpu("1m") == 1


def test_whole_cores():
    assert broken.parse_cpu("1") == 1000
    assert broken.parse_cpu("2") == 2000


def test_fractional_cores():
    assert broken.parse_cpu("1.5") == 1500
    assert broken.parse_cpu("0.1") == 100


def test_float_noise_does_not_lose_a_millicore():
    assert broken.parse_cpu("1.001") == 1001, "1.001 * 1000 is 1000.9999999999999; round, do not truncate"


def test_invalid_quantity_rejected():
    for bad in ("", "abc", "1 core", "-1", "m"):
        with pytest.raises(ValueError):
            broken.parse_cpu(bad)


def test_pod_sums_all_containers():
    pod = {"containers": [{"cpu": "250m"}, {"cpu": "0.5"}, {"name": "pause"}]}
    assert broken.pod_millicores(pod) == 750


def test_namespace_totals():
    pods = [
        {"namespace": "billing", "containers": [{"cpu": "1"}, {"cpu": "100m"}]},
        {"namespace": "billing", "containers": [{"cpu": "400m"}]},
        {"namespace": "search", "containers": [{"cpu": "2"}]},
        {"containers": [{"cpu": "50m"}]},
    ]
    assert broken.namespace_totals(pods) == {"billing": 1500, "search": 2000, "default": 50}
