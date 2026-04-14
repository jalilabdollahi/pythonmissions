import pytest
import sys
sys.path.insert(0, ".")
from broken import validate_deployment

VALID = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {"name": "myapp"},
    "spec": {"replicas": 3},
}

def test_valid_manifest():
    errors = validate_deployment(VALID)
    assert errors == []

def test_missing_field():
    bad = {k: v for k, v in VALID.items() if k != "spec"}
    errors = validate_deployment(bad)
    assert any("spec" in e for e in errors)

def test_string_replicas():
    bad = {**VALID, "spec": {"replicas": "3"}}
    errors = validate_deployment(bad)
    assert any("integer" in e for e in errors)

def test_missing_name():
    bad = {**VALID, "metadata": {}}
    errors = validate_deployment(bad)
    assert any("name" in e for e in errors)
