import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def build(tmp_path):
    (tmp_path / "a.log").write_bytes(b"x" * 10)
    (tmp_path / "Makefile").write_bytes(b"x" * 4)
    sub = tmp_path / "build" / "deep"
    sub.mkdir(parents=True)
    (sub / "out.bin").write_bytes(b"x" * 100)
    (tmp_path / "build" / "b.LOG").write_bytes(b"x" * 5)
    (tmp_path / "build" / "c.txt").write_bytes(b"x" * 7)
    return str(tmp_path)


def test_files_in_the_top_directory_are_counted(tmp_path):
    (tmp_path / "one.txt").write_bytes(b"123")
    assert broken.usage_by_extension(str(tmp_path)) == {".txt": 3}


def test_nested_directories_are_walked(tmp_path):
    totals = broken.usage_by_extension(build(tmp_path))
    assert totals[".bin"] == 100, "files in subfolders must be found by their full path"


def test_extensions_are_case_insensitive(tmp_path):
    totals = broken.usage_by_extension(build(tmp_path))
    assert totals[".log"] == 15
    assert ".LOG" not in totals


def test_extensionless_files_use_none_bucket(tmp_path):
    totals = broken.usage_by_extension(build(tmp_path))
    assert totals["(none)"] == 4
    assert "" not in totals


def test_full_result(tmp_path):
    assert broken.usage_by_extension(build(tmp_path)) == {
        ".log": 15, "(none)": 4, ".bin": 100, ".txt": 7,
    }


def test_empty_tree(tmp_path):
    assert broken.usage_by_extension(str(tmp_path)) == {}


def test_top_extensions_ranking_and_tie_break():
    totals = {".a": 5, ".b": 9, ".c": 5, ".d": 1}
    assert broken.top_extensions(totals, 3) == [(".b", 9), (".a", 5), (".c", 5)]
