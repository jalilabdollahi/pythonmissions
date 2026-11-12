import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import read_changelog, write_summary


def test_reads_accented_names(tmp_path):
    path = tmp_path / "CHANGELOG.md"
    path.write_bytes("Thanks to Zoë and José\n".encode("utf-8"))
    assert read_changelog(path) == "Thanks to Zoë and José\n"


def test_reads_arrows_and_checkmarks(tmp_path):
    path = tmp_path / "CHANGELOG.md"
    path.write_bytes("v1 → v2 ✓\n".encode("utf-8"))
    assert read_changelog(path) == "v1 → v2 ✓\n", "the file is UTF-8"


def test_summary_is_written_as_utf8(tmp_path):
    path = tmp_path / "summary.txt"
    write_summary(path, ["deploy → prod", "café menu fixed"])
    assert path.read_bytes() == "deploy → prod\ncafé menu fixed\n".encode("utf-8")


def test_summary_with_plain_ascii(tmp_path):
    path = tmp_path / "summary.txt"
    write_summary(path, ["one", "two"])
    assert path.read_text(encoding="utf-8") == "one\ntwo\n"


def test_round_trip_keeps_text(tmp_path):
    path = tmp_path / "summary.txt"
    write_summary(path, ["Zoë → ✓"])
    assert read_changelog(path) == "Zoë → ✓\n"
