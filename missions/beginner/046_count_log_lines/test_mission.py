import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import last_lines, summarize_log


def make_log(tmp_path):
    path = tmp_path / "error.log"
    path.write_text(
        "INFO worker started\n"
        "ERROR upstream timed out\n"
        "INFO request ok\n"
        "ERROR connection reset\n"
        "ERROR disk quota\n",
        encoding="utf-8",
    )
    return path


def test_total_line_count(tmp_path):
    total, _ = summarize_log(make_log(tmp_path))
    assert total == 5, "every line in the file must be counted"


def test_error_line_count(tmp_path):
    _, errors = summarize_log(make_log(tmp_path))
    assert errors == 3


def test_empty_log(tmp_path):
    path = tmp_path / "empty.log"
    path.write_text("", encoding="utf-8")
    assert summarize_log(path) == (0, 0)


def test_last_lines_returns_tail(tmp_path):
    assert last_lines(make_log(tmp_path), 2) == ["ERROR connection reset", "ERROR disk quota"]


def test_last_zero_lines(tmp_path):
    assert last_lines(make_log(tmp_path), 0) == []
