import pytest, sys
sys.path.insert(0, ".")
from broken import merge_helm_values, apply_env_values

BASE = {"replicaCount": 1, "image": {"tag": "latest", "repo": "myapp"}}
OVERRIDE = {"replicaCount": 3, "image": {"tag": "v2.0"}}

def test_shallow_values():
    result = merge_helm_values(BASE, OVERRIDE)
    assert result["replicaCount"] == 3

def test_deep_merge():
    result = merge_helm_values(BASE, OVERRIDE)
    assert result["image"]["tag"] == "v2.0"
    assert result["image"]["repo"] == "myapp"  # preserved from base

def test_no_mutation():
    import copy
    base_copy = copy.deepcopy(BASE)
    merge_helm_values(BASE, OVERRIDE)
    assert BASE == base_copy
