import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import load_hostnames, is_registered, unregistered


def make_file(tmp_path, text):
    path = tmp_path / "edges.txt"
    path.write_text(text)
    return path


def test_hostnames_have_no_newline(tmp_path):
    path = make_file(tmp_path, "edge-01\nedge-02\n")
    assert load_hostnames(path) == ["edge-01", "edge-02"], "entries must not keep their trailing newline"


def test_last_line_without_newline(tmp_path):
    path = make_file(tmp_path, "edge-01\nedge-02")
    assert load_hostnames(path) == ["edge-01", "edge-02"]


def test_blank_lines_and_spaces_are_skipped(tmp_path):
    path = make_file(tmp_path, "edge-01  \n\n   \n edge-02\n")
    assert load_hostnames(path) == ["edge-01", "edge-02"]


def test_membership_check(tmp_path):
    path = make_file(tmp_path, "edge-01\nedge-02\n")
    assert is_registered("edge-02", path) is True
    assert is_registered("edge-09", path) is False


def test_unregistered_keeps_input_order(tmp_path):
    path = make_file(tmp_path, "edge-01\nedge-02\n")
    assert unregistered(["edge-07", "edge-01", "edge-05"], path) == ["edge-07", "edge-05"]
