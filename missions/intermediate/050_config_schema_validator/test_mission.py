import pytest
import sys
sys.path.insert(0, ".")
from broken import validate_config, is_valid

VALID_CONFIG = {"host": "localhost", "port": 8080, "debug": False, "workers": 4}

def test_valid_config():
    assert validate_config(VALID_CONFIG) == []
    assert is_valid(VALID_CONFIG) is True

def test_missing_key():
    cfg = {k: v for k, v in VALID_CONFIG.items() if k != "port"}
    errors = validate_config(cfg)
    assert any("port" in e for e in errors)

def test_wrong_type():
    cfg = {**VALID_CONFIG, "port": "8080"}
    errors = validate_config(cfg)
    assert any("port" in e for e in errors)

def test_multiple_errors():
    cfg = {"host": "localhost"}  # missing port, debug, workers
    errors = validate_config(cfg)
    assert len(errors) >= 3  # all missing keys reported
