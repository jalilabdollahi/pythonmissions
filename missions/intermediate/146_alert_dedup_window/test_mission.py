import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def alert(ts, name="HighLatency", **labels):
    return {"name": name, "labels": labels or {"host": "db1", "disk": "sda"}, "ts": ts}


def test_first_alert_is_sent():
    assert broken.AlertDeduper(60).should_send(alert(0)) is True


def test_label_order_does_not_change_fingerprint():
    a = {"name": "Down", "labels": {"host": "a", "dc": "x"}, "ts": 0}
    b = {"name": "Down", "labels": {"dc": "x", "host": "a"}, "ts": 1}
    assert broken.fingerprint(a) == broken.fingerprint(b), "same labels in another order are the same alert"
    d = broken.AlertDeduper(60)
    assert d.should_send(a) is True
    assert d.should_send(b) is False


def test_repeat_inside_window_is_suppressed():
    d = broken.AlertDeduper(60)
    d.should_send(alert(0))
    assert d.should_send(alert(59)) is False


def test_repeat_exactly_at_window_edge_is_sent():
    d = broken.AlertDeduper(60)
    d.should_send(alert(0))
    assert d.should_send(alert(60)) is True, "window is exclusive: at +60s a new page goes out"


def test_window_is_measured_from_last_sent_not_last_seen():
    d = broken.AlertDeduper(60)
    sent = d.filter([alert(t) for t in (0, 30, 60, 90, 120)])
    assert [a["ts"] for a in sent] == [0, 60, 120], "suppressed alerts must not extend the window"


def test_different_labels_are_different_alerts():
    d = broken.AlertDeduper(60)
    assert d.should_send(alert(0, host="a")) is True
    assert d.should_send(alert(1, host="b")) is True
    assert d.should_send(alert(2, name="Other", host="a")) is True


def test_suppressed_counts():
    d = broken.AlertDeduper(60)
    d.filter([alert(0), alert(10), alert(20), alert(70)])
    assert d.total_suppressed() == 2
