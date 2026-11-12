import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_creates_a_new_file(tmp_path):
    target = tmp_path / "proxy.json"
    broken.atomic_write_text(target, "hello")
    assert target.read_text() == "hello"


def test_replaces_existing_content_and_leaves_no_temp_files(tmp_path):
    target = tmp_path / "proxy.json"
    target.write_text("old")
    broken.atomic_write_text(target, "new")
    assert target.read_text() == "new"
    assert os.listdir(tmp_path) == ["proxy.json"]


def test_temp_file_lives_in_the_target_directory(tmp_path, monkeypatch):
    target = tmp_path / "proxy.json"
    seen = []
    real_replace = os.replace

    def spy(src, dst):
        seen.append((os.path.dirname(os.path.abspath(src)), os.path.dirname(os.path.abspath(dst))))
        return real_replace(src, dst)

    monkeypatch.setattr(os, "replace", spy)
    broken.atomic_write_text(target, "x")
    (src_dir, dst_dir), = seen
    assert os.path.samefile(src_dir, dst_dir), "os.replace is only atomic on one filesystem"


def test_data_is_synced_before_the_swap(tmp_path, monkeypatch):
    events = []
    real_fsync, real_replace = os.fsync, os.replace
    monkeypatch.setattr(os, "fsync", lambda fd: (events.append("fsync"), real_fsync(fd))[1])
    monkeypatch.setattr(os, "replace", lambda a, b: (events.append("replace"), real_replace(a, b))[1])
    broken.atomic_write_text(tmp_path / "f", "data")
    assert events == ["fsync", "replace"]


def test_failed_write_keeps_old_content(tmp_path):
    target = tmp_path / "proxy.json"
    target.write_text("precious")
    with pytest.raises(TypeError):
        broken.atomic_write_text(target, 12345)
    assert target.read_text() == "precious"


def test_failed_write_leaves_no_temp_file(tmp_path):
    target = tmp_path / "proxy.json"
    with pytest.raises(TypeError):
        broken.atomic_write_text(target, None)
    assert os.listdir(tmp_path) == [], "temporary files must be cleaned up on errors"


def test_update_config_merges_into_json(tmp_path):
    target = tmp_path / "proxy.json"
    target.write_text(json.dumps({"port": 80, "tls": False}))
    result = broken.update_config(target, {"tls": True, "region": "eu"})
    assert result == {"port": 80, "tls": True, "region": "eu"}
    assert json.loads(target.read_text()) == result


def test_update_config_creates_missing_file(tmp_path):
    target = tmp_path / "new.json"
    broken.update_config(target, {"a": 1})
    assert json.loads(target.read_text()) == {"a": 1}
