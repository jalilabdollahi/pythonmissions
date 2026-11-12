import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import append_and_count, stage_manifest


def test_manifest_verifies_after_write(tmp_path):
    path = tmp_path / "manifest.json"
    assert stage_manifest(path, '{"build": 42}') is True, "reading back must see the data just written"


def test_manifest_content_is_on_disk(tmp_path):
    path = tmp_path / "manifest.json"
    stage_manifest(path, "abc")
    assert path.read_text(encoding="utf-8") == "abc"


def test_manifest_overwrites_old_content(tmp_path):
    path = tmp_path / "manifest.json"
    path.write_text("old old old old", encoding="utf-8")
    assert stage_manifest(path, "new") is True
    assert path.read_text(encoding="utf-8") == "new"


def test_append_and_count_includes_new_line(tmp_path):
    path = tmp_path / "queue.txt"
    path.write_text("a\nb\n", encoding="utf-8")
    assert append_and_count(path, "c") == 3, "the count must include the line just appended"


def test_append_and_count_on_new_file(tmp_path):
    path = tmp_path / "fresh.txt"
    assert append_and_count(path, "first") == 1
    assert append_and_count(path, "second") == 2
