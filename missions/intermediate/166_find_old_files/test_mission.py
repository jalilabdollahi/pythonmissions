import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

DAY = 86400
NOW = 2_000_000_000


def touch(path, age_days, content=b"x"):
    path.write_bytes(content)
    stamp = NOW - age_days * DAY
    os.utime(path, (stamp, stamp))


def test_old_files_are_listed_and_recent_ones_are_not(tmp_path):
    touch(tmp_path / "rc-old.tar", 40)
    touch(tmp_path / "rc-new.tar", 0.04)
    assert broken.find_old_files(str(tmp_path), 30, NOW) == ["rc-old.tar"]


def test_a_day_is_86400_seconds(tmp_path):
    touch(tmp_path / "two-days.tar", 2)
    assert broken.find_old_files(str(tmp_path), 7, NOW) == [], "2 days old is not older than 7 days"


def test_file_exactly_at_the_limit_is_kept(tmp_path):
    touch(tmp_path / "edge.tar", 30)
    assert broken.find_old_files(str(tmp_path), 30, NOW) == []


def test_just_over_the_limit_is_listed(tmp_path):
    path = tmp_path / "over.tar"
    path.write_bytes(b"x")
    stamp = NOW - 30 * DAY - 1
    os.utime(path, (stamp, stamp))
    assert broken.find_old_files(str(tmp_path), 30, NOW) == ["over.tar"]


def test_directories_are_never_listed(tmp_path):
    folder = tmp_path / "releases"
    folder.mkdir()
    stamp = NOW - 90 * DAY
    os.utime(folder, (stamp, stamp))
    touch(tmp_path / "old.zip", 90)
    assert broken.find_old_files(str(tmp_path), 30, NOW) == ["old.zip"]


def test_result_is_sorted(tmp_path):
    for name in ("c", "a", "b"):
        touch(tmp_path / name, 100)
    assert broken.find_old_files(str(tmp_path), 1, NOW) == ["a", "b", "c"]


def test_total_size_adds_named_files(tmp_path):
    touch(tmp_path / "a", 100, b"12345")
    touch(tmp_path / "b", 100, b"123")
    assert broken.total_size(str(tmp_path), ["a", "b"]) == 8
