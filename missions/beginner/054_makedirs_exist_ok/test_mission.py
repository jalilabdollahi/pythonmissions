import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_creates_missing_base_directory(tmp_path):
    base = tmp_path / "deep" / "releases"
    release = broken.prepare_release(base, "1.0")
    assert (release / "logs").is_dir(), "parents must be created when the base is missing"


def test_second_run_for_same_version_succeeds(tmp_path):
    broken.prepare_release(tmp_path, "1.0")
    broken.prepare_release(tmp_path, "1.0")


def test_existing_files_survive_a_rerun(tmp_path):
    release = broken.prepare_release(tmp_path, "1.0")
    (release / "app.bin").write_text("data")
    broken.prepare_release(tmp_path, "1.0")
    assert (release / "app.bin").read_text() == "data"


def test_list_releases_sorted(tmp_path):
    broken.prepare_release(tmp_path, "b")
    broken.prepare_release(tmp_path, "a")
    assert broken.list_releases(tmp_path) == ["a", "b"]


def test_mark_current_can_be_repeated(tmp_path):
    broken.mark_current(tmp_path, "3.1")
    marker = broken.mark_current(tmp_path, "3.1")
    assert marker.read_text() == "3.1\n"


def test_existing_release_dir_without_logs_gets_logs(tmp_path):
    (tmp_path / "7.7").mkdir()
    release = broken.prepare_release(tmp_path, "7.7")
    assert (release / "logs").is_dir()
