import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_latency_summary_from_a_list():
    lines = ["GET /pay 120", "GET /pay 80", "POST /pay 300"]
    assert broken.latency_summary(lines) == {"count": 3, "min": 80, "max": 300}


def test_latency_summary_accepts_a_generator():
    gen = (line for line in ["GET /a 5", "", "GET /b 9"])
    assert broken.latency_summary(gen) == {"count": 2, "min": 5, "max": 9}, "a generator can only be read once"


def test_latency_summary_empty():
    assert broken.latency_summary(iter([])) == {"count": 0, "min": None, "max": None}


def test_error_report_counts_lines_and_errors(tmp_path):
    log = tmp_path / "deploy.log"
    log.write_text("start\nERROR disk full\nok\nERROR timeout\n")
    total, errors = broken.error_report(log)
    assert total == 4
    assert errors == ["ERROR disk full", "ERROR timeout"], "the file handle was already consumed by the first pass"


def test_error_report_without_errors(tmp_path):
    log = tmp_path / "clean.log"
    log.write_text("a\nb\n")
    assert broken.error_report(log) == (2, [])


def test_recent_failures_keeps_every_failed_event():
    events = [{"id": 1, "ok": False}, {"id": 2, "ok": True}, {"id": 3, "ok": False}]
    assert [e["id"] for e in broken.recent_failures(iter(events))] == [1, 3], "checking for failures must not eat the first one"


def test_recent_failures_empty():
    assert broken.recent_failures([{"id": 1, "ok": True}]) == []
