import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_substitutes():
    from broken import render_alert
    tmpl = "Alert: $level on $host"
    vals = {"level": "CRITICAL", "host": "web-01"}
    result = render_alert(tmpl, vals)
    assert result == "Alert: CRITICAL on web-01"

def test_message():
    from broken import render_alert
    tmpl = "$host: $msg"
    result = render_alert(tmpl, {"host": "db-01", "msg": "OOM"})
    assert result == "db-01: OOM"
