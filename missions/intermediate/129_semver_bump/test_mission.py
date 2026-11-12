import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_patch_bump():
    assert broken.bump("2.4.7", "patch") == "2.4.8"


def test_minor_bump_resets_patch():
    assert broken.bump("2.4.7", "minor") == "2.5.0", "lower parts reset to zero"


def test_major_bump_resets_minor_and_patch():
    assert broken.bump("2.4.7", "major") == "3.0.0"


def test_prerelease_is_parsed_and_dropped_by_bump():
    assert broken.parse("1.2.3-rc.1") == (1, 2, 3, "rc.1")
    assert broken.bump("v1.2.3-rc.1", "patch") == "1.2.4"
    assert broken.parse("1.2.3+build.5") == (1, 2, 3, None)


def test_unknown_part_and_garbage_rejected():
    with pytest.raises(ValueError):
        broken.bump("1.2.3", "micro")
    with pytest.raises(ValueError):
        broken.parse("1.2")


def test_latest_compares_numbers_not_strings():
    assert broken.latest(["1.9.0", "1.10.0", "1.2.0"]) == "1.10.0"


def test_release_beats_its_own_prerelease():
    assert broken.latest(["2.0.0-rc.1", "2.0.0", "1.9.9"]) == "2.0.0"


def test_latest_empty_raises():
    with pytest.raises(ValueError):
        broken.latest([])
