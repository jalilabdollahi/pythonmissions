import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import AUDIT, audited_alert, prefixed_alert, send_alert


def test_core_sender_defaults():
    assert send_alert("#ops", "hi") == {"channel": "#ops", "message": "hi", "severity": "info", "sent": True}


def test_prefix_is_added():
    assert prefixed_alert("#ops", "disk full")["message"] == "[ops] disk full"


def test_severity_reaches_core_sender():
    assert prefixed_alert("#ops", "db down", severity="critical")["severity"] == "critical"


def test_dry_run_reaches_core_sender():
    assert prefixed_alert("#ops", "drill", dry_run=True)["sent"] is False, "dry runs must not send"


def test_audit_decorator_forwards_keyword_options():
    result = audited_alert("#ops", "drill", severity="warn", dry_run=True)
    assert result["severity"] == "warn"
    assert result["sent"] is False


def test_audit_decorator_records_calls():
    AUDIT.clear()
    audited_alert("#ops", "x")
    assert AUDIT == ["prefixed_alert"]
