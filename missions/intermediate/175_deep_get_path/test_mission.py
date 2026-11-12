import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


POD = {
    "metadata": {"name": "web"},
    "spec": {
        "replicas": 0,
        "paused": False,
        "containers": [{"name": "app", "image": "app:1.2"}, {"name": "side", "image": "envoy:v3"}],
    },
    "ports": {"80": "http", "443": "https"},
}


def test_reads_list_index_in_path():
    assert broken.deep_get(POD, "spec.containers.0.image") == "app:1.2"
    assert broken.deep_get(POD, "spec.containers.1.name") == "side"


def test_missing_key_returns_default():
    assert broken.deep_get(POD, "spec.nodeSelector.disk") is None
    assert broken.deep_get(POD, "spec.nodeSelector.disk", "ssd") == "ssd"


def test_zero_and_false_are_real_values():
    assert broken.deep_get(POD, "spec.replicas", 1) == 0, "replicas=0 is a value, not a missing key"
    assert broken.deep_get(POD, "spec.paused", True) is False


def test_numeric_looking_dict_keys_stay_strings():
    assert broken.deep_get(POD, "ports.80") == "http"
    assert broken.deep_get(POD, "ports.443") == "https"


def test_negative_index_counts_from_the_end():
    assert broken.deep_get(POD, "spec.containers.-1.image") == "envoy:v3"


def test_out_of_range_and_bad_index_return_default():
    assert broken.deep_get(POD, "spec.containers.5.image", "none") == "none"
    assert broken.deep_get(POD, "spec.containers.-9.image", "none") == "none"
    assert broken.deep_get(POD, "spec.containers.first.image", "none") == "none"


def test_cannot_descend_into_a_scalar():
    assert broken.deep_get(POD, "metadata.name.first", "d") == "d"


def test_container_images():
    assert broken.container_images(POD) == ["app:1.2", "envoy:v3"]
    assert broken.container_images({}) == []
