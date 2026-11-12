import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def make_logs(tmp_path, **contents):
    base = tmp_path / "audit.log"
    for suffix, text in contents.items():
        name = "audit.log" if suffix == "live" else f"audit.log.{suffix[1:]}"
        (tmp_path / name).write_text(text)
    return str(base)


def read(path):
    with open(path) as handle:
        return handle.read()


def test_backups_shift_without_overwriting_each_other(tmp_path):
    base = make_logs(tmp_path, live="now", b1="one", b2="two", b3="three")
    broken.rotate(base, keep=3)
    assert read(base + ".1") == "now"
    assert read(base + ".2") == "one", "old .1 must move to .2 before .1 is reused"
    assert read(base + ".3") == "two"


def test_oldest_backup_is_dropped(tmp_path):
    base = make_logs(tmp_path, live="now", b1="one", b2="two", b3="three")
    broken.rotate(base, keep=3)
    assert not os.path.exists(base + ".4")
    assert "three" not in [read(base + f".{i}") for i in (1, 2, 3)]


def test_fresh_empty_live_file_exists_after_rotation(tmp_path):
    base = make_logs(tmp_path, live="now")
    broken.rotate(base)
    assert os.path.exists(base)
    assert read(base) == ""


def test_first_rotation_with_no_backups(tmp_path):
    base = make_logs(tmp_path, live="first")
    broken.rotate(base, keep=2)
    assert read(base + ".1") == "first"
    assert not os.path.exists(base + ".2")


def test_keep_one_replaces_previous_backup(tmp_path):
    base = make_logs(tmp_path, live="new", b1="old")
    broken.rotate(base, keep=1)
    assert read(base + ".1") == "new"


def test_needs_rotation_at_exact_limit(tmp_path):
    base = make_logs(tmp_path, live="12345")
    assert broken.needs_rotation(base, 5) is True, "a file that reached the limit is full"
    assert broken.needs_rotation(base, 6) is False


def test_needs_rotation_missing_file(tmp_path):
    assert broken.needs_rotation(str(tmp_path / "nope.log"), 1) is False


def test_maybe_rotate_reports_what_it_did(tmp_path):
    base = make_logs(tmp_path, live="abcdef")
    assert broken.maybe_rotate(base, 100) is False
    assert broken.maybe_rotate(base, 6) is True
    assert read(base + ".1") == "abcdef"
