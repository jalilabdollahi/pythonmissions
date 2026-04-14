import pytest
import sys
sys.path.insert(0, ".")
from broken import parse_manifest, get_replicas

MANIFEST = """
apiVersion: apps/v1
kind: Deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
"""

def test_parse_manifest():
    data = parse_manifest(MANIFEST)
    assert data["kind"] == "Deployment"
    assert data["spec"]["replicas"] == 3

def test_get_replicas():
    assert get_replicas(MANIFEST) == 3

def test_get_replicas_default():
    assert get_replicas("apiVersion: v1\nkind: Service") == 1
