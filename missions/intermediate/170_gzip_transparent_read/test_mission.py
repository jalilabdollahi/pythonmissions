import gzip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

LINES = "2024-05-01T10:00:00 ERROR disk full\n2024-05-01T10:00:01 INFO retry\n2024-05-01T10:00:02 ERROR disk full\n"


def write_plain(path, text=LINES):
    path.write_text(text, encoding="utf-8")
    return str(path)


def write_gz(path, text=LINES):
    with gzip.open(path, "wt", encoding="utf-8") as handle:
        handle.write(text)
    return str(path)


def test_plain_log_is_read_as_text(tmp_path):
    with broken.open_log(write_plain(tmp_path / "app.log")) as handle:
        assert handle.readline().startswith("2024-05-01T10:00:00 ERROR")


def test_gzip_log_is_read_as_text_not_bytes(tmp_path):
    with broken.open_log(write_gz(tmp_path / "app.log.gz")) as handle:
        first = handle.readline()
    assert isinstance(first, str), "gzip.open needs text mode"
    assert "ERROR" in first


def test_compression_is_detected_by_content_not_name(tmp_path):
    with broken.open_log(write_gz(tmp_path / "app.log.1")) as handle:
        assert "disk full" in handle.read()


def test_plain_file_with_gz_name_is_still_plain(tmp_path):
    with broken.open_log(write_plain(tmp_path / "old.gz")) as handle:
        assert "INFO" in handle.read()


def test_count_levels_across_mixed_files(tmp_path):
    paths = [write_plain(tmp_path / "a.log"), write_gz(tmp_path / "b.log.gz"), write_gz(tmp_path / "c.log.2")]
    assert broken.count_levels(paths) == {"ERROR": 6, "INFO": 3}


def test_blank_and_short_lines_are_skipped(tmp_path):
    text = LINES + "\n   \nlonely\n"
    assert broken.count_levels([write_plain(tmp_path / "x.log", text)]) == {"ERROR": 2, "INFO": 1}


def test_empty_file_counts_nothing(tmp_path):
    assert broken.count_levels([write_plain(tmp_path / "e.log", "")]) == {}
