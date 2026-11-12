import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def write_csv(tmp_path):
    p = tmp_path / "traffic.csv"
    p.write_text("host,requests\nweb-1,100\nweb-2,300\nweb-3,200\n")
    return p


def test_load_rows_excludes_header(tmp_path):
    rows = broken.load_rows(write_csv(tmp_path))
    assert rows[0] == ["web-1", "100"], "the header row is not data"
    assert len(rows) == 3


def test_host_count(tmp_path):
    assert broken.host_count(write_csv(tmp_path)) == 3


def test_total_requests(tmp_path):
    assert broken.total_requests(write_csv(tmp_path)) == 600


def test_busiest_host(tmp_path):
    assert broken.busiest_host(write_csv(tmp_path)) == "web-2"


def test_average_requests(tmp_path):
    assert broken.average_requests(write_csv(tmp_path)) == 200


def test_header_only_file_has_no_hosts(tmp_path):
    p = tmp_path / "empty.csv"
    p.write_text("host,requests\n")
    assert broken.host_count(p) == 0
