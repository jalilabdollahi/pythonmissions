import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_format_alert():
    from broken import format_alert
    assert format_alert("CRITICAL", "Disk full") == "[CRITICAL] Disk full"

def test_warn_level():
    from broken import format_alert
    assert format_alert("WARN", "High CPU") == "[WARN] High CPU"
