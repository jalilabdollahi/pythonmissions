import pytest
import sys
sys.path.insert(0, ".")
from broken import merge_configs, deep_merge

def test_merge_configs():
    base = {"host": "localhost", "port": 80}
    override = {"port": 443, "ssl": True}
    result = merge_configs(base, override)
    assert result["port"] == 443
    assert result["host"] == "localhost"
    assert result["ssl"] is True

def test_deep_merge():
    base = {"db": {"host": "localhost", "port": 5432}}
    override = {"db": {"port": 5433}}
    result = deep_merge(base, override)
    assert result["db"]["port"] == 5433
    assert result["db"]["host"] == "localhost"
