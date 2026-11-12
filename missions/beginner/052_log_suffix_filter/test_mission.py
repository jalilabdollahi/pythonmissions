import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def make_dir(tmp_path):
    (tmp_path / "app.log").write_text("aaaa")
    (tmp_path / "error.log").write_text("bb")
    (tmp_path / "catalog").write_text("keep me")
    (tmp_path / "syslog").write_text("keep me too")
    (tmp_path / "notes.txt").write_text("x")
    (tmp_path / "old.log.gz").write_text("zz")
    (tmp_path / "sub.log").mkdir()
    return tmp_path


def test_find_logs_returns_only_dot_log_files(tmp_path):
    make_dir(tmp_path)
    assert broken.find_logs(tmp_path) == ["app.log", "error.log"]


def test_catalog_is_not_a_log(tmp_path):
    make_dir(tmp_path)
    assert "catalog" not in broken.find_logs(tmp_path), "endswith('log') also matches catalog"


def test_total_bytes_counts_only_logs(tmp_path):
    make_dir(tmp_path)
    assert broken.total_log_bytes(tmp_path) == 6


def test_delete_keeps_lookalikes(tmp_path):
    make_dir(tmp_path)
    assert broken.delete_logs(tmp_path) == 2
    assert (tmp_path / "catalog").exists()
    assert (tmp_path / "syslog").exists()
    assert not (tmp_path / "app.log").exists()
