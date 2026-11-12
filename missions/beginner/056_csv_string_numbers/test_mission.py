import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

ROWS = [
    {"service": "ingest", "bytes": "100", "latency_ms": "9"},
    {"service": "ingest", "bytes": "250", "latency_ms": "40"},
    {"service": "export", "bytes": "5000", "latency_ms": "120"},
]


def test_bytes_are_summed_as_numbers():
    assert broken.bytes_by_service(ROWS)["ingest"] == 350, "'100' + '250' joins text instead of adding"


def test_totals_are_integers():
    assert isinstance(broken.bytes_by_service(ROWS)["export"], int)


def test_slowest_row_compares_numbers_not_text():
    assert broken.slowest_row(ROWS)["service"] == "export", "'9' > '120' only when comparing text"


def test_busiest_service():
    assert broken.busiest_service(ROWS) == "export"


def test_report_format():
    assert broken.report(ROWS) == "export: 5000 bytes\ningest: 350 bytes"


def test_load_reads_file(tmp_path):
    p = tmp_path / "cost.csv"
    p.write_text("service,bytes,latency_ms\na,1,2\n")
    assert broken.load(p) == [{"service": "a", "bytes": "1", "latency_ms": "2"}]
