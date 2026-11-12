import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

GI = 1024**3


def test_binary_suffixes():
    assert broken.parse_memory("512Mi") == 512 * 1024**2
    assert broken.parse_memory("2Gi") == 2 * GI
    assert broken.parse_memory("64Ki") == 65536


def test_decimal_suffixes_are_powers_of_1000():
    assert broken.parse_memory("1G") == 1_000_000_000
    assert broken.parse_memory("500M") == 500_000_000
    assert broken.parse_memory("2K") == 2000


def test_no_suffix_is_bytes():
    assert broken.parse_memory("1048576") == 1048576


def test_fractions_are_multiplied_before_truncating():
    assert broken.parse_memory("1.5Gi") == GI + GI // 2
    assert broken.parse_memory("0.5Mi") == 524288


def test_invalid_quantities():
    for bad in ("", "Gi", "12 Mi", "1gi", "-5Mi", "3Pi"):
        with pytest.raises(ValueError):
            broken.parse_memory(bad)


def test_total_requests_ignores_missing_values():
    pods = [
        {"containers": [{"memory": "256Mi"}, {"name": "sidecar"}]},
        {"containers": [{"memory": "1Gi"}]},
    ]
    assert broken.total_requests(pods) == 256 * 1024**2 + GI


def test_exact_fit_is_allowed():
    pods = [{"containers": [{"memory": "2Gi"}, {"memory": "2Gi"}]}]
    assert broken.fits_on_node(pods, 4 * GI), "requests equal to capacity still fit"
    assert not broken.fits_on_node(pods, 4 * GI - 1)
