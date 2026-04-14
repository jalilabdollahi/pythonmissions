import pytest, sys
sys.path.insert(0, ".")
from broken import log_event, log_info

def test_log_fields():
    record = log_event("INFO", "server started", service="api")
    assert record.get("level") == "INFO"
    assert "timestamp" in record
    assert "msg" in record

def test_log_info():
    record = log_info("deploy complete", version="v2")
    assert record["level"] == "INFO"
    assert record["msg"] == "deploy complete"
