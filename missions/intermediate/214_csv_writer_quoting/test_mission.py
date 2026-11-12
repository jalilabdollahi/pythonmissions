import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

ROWS = [
    {"host": "web1", "status": "pass", "note": "ok"},
    {"host": "db1", "status": "warn", "note": "disk 91%, rotating logs"},
    {"host": "db2", "status": "fail", "note": 'said "no" twice'},
    {"host": "app1", "status": "fail", "note": "line one\r\nline two"},
]


def test_first_line_is_the_header(tmp_path):
    path = tmp_path / "audit.csv"
    broken.write_report(path, ROWS)
    first = path.read_bytes().splitlines()[0]
    assert first == b"host,status,note"


def test_commas_in_notes_are_quoted(tmp_path):
    path = tmp_path / "audit.csv"
    broken.write_report(path, ROWS)
    text = path.read_text(encoding="utf-8", newline="")
    assert '"disk 91%, rotating logs"' in text


def test_roundtrip_preserves_every_field(tmp_path):
    path = tmp_path / "audit.csv"
    broken.write_report(path, ROWS)
    assert broken.read_report(path) == ROWS


def test_embedded_line_breaks_survive_reading(tmp_path):
    path = tmp_path / "audit.csv"
    broken.write_report(path, ROWS)
    notes = {row["host"]: row["note"] for row in broken.read_report(path)}
    assert notes["app1"] == "line one\r\nline two", "open the file with newline='' when reading"


def test_append_row_adds_without_a_second_header(tmp_path):
    path = tmp_path / "audit.csv"
    broken.write_report(path, ROWS[:1])
    broken.append_row(path, {"host": "x", "status": "pass", "note": "a, b"})
    assert broken.read_report(path) == [ROWS[0], {"host": "x", "status": "pass", "note": "a, b"}]


def test_status_counts(tmp_path):
    path = tmp_path / "audit.csv"
    broken.write_report(path, ROWS)
    assert broken.status_counts(path) == {"pass": 1, "warn": 1, "fail": 2}


def test_failing_hosts_exclude_passes(tmp_path):
    path = tmp_path / "audit.csv"
    broken.write_report(path, ROWS)
    assert broken.failing_hosts(path) == ["app1", "db1", "db2"]


def test_empty_export_still_has_header(tmp_path):
    path = tmp_path / "empty.csv"
    broken.write_report(path, [])
    assert broken.read_report(path) == []
    assert path.read_text(encoding="utf-8").strip() == "host,status,note"
