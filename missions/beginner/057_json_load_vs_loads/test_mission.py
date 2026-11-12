import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json

import broken


def test_parse_event_reads_a_json_string():
    event = broken.parse_event('{"id": 7, "severity": "high"}')
    assert event == {"id": 7, "severity": "high"}


def test_parse_event_defaults_missing_severity():
    assert broken.parse_event('{"id": 1}')["severity"] == "unknown"


def test_load_events_reads_a_file(tmp_path):
    p = tmp_path / "events.json"
    p.write_text(json.dumps([{"id": 1, "severity": "low"}, {"id": 2, "severity": "high"}]))
    assert [e["id"] for e in broken.load_events(p)] == [1, 2]


def test_severities_are_distinct_and_sorted():
    events = [{"severity": "low"}, {"severity": "high"}, {"severity": "low"}, {}]
    assert broken.severities(events) == ["high", "low", "unknown"]


def test_worst_first_ordering():
    events = [{"id": 1, "severity": "low"}, {"id": 2, "severity": "critical"}]
    assert [e["id"] for e in broken.worst_first(events)] == [2, 1]
