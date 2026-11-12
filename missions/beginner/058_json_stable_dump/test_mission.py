import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_manifest_sorts_keys():
    a = broken.render_manifest({"b": 1, "a": 2})
    b = broken.render_manifest({"a": 2, "b": 1})
    assert a == b, "same content must render to the same text"


def test_manifest_sorts_nested_keys():
    text = broken.render_manifest({"outer": {"z": 1, "a": 2}})
    assert text.index('"a"') < text.index('"z"')


def test_snapshot_is_indented_one_key_per_line():
    text = broken.render_snapshot({"a": 1, "b": 2})
    assert text == '{\n  "a": 1,\n  "b": 2\n}'


def test_write_snapshot_has_trailing_newline(tmp_path):
    p = tmp_path / "snap.json"
    broken.write_snapshot(p, {"k": "v"})
    assert p.read_text() == '{\n  "k": "v"\n}\n'


def test_reordered_config_is_not_a_change():
    assert broken.has_changed({"a": 1, "b": 2}, {"b": 2, "a": 1}) is False
    assert broken.has_changed({"a": 1}, {"a": 2}) is True


def test_line_count_reflects_indentation():
    assert broken.line_count({"a": 1, "b": 2}) == 4
