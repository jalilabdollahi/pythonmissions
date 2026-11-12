import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

import broken


def test_single_spaced_command():
    assert broken.parse_command("deploy web v2") == ("deploy", "web", ["v2"])


def test_double_spaces_between_words():
    assert broken.parse_command("deploy  web   v2") == ("deploy", "web", ["v2"]), "extra spaces create empty words"


def test_tabs_and_edges_are_ignored():
    assert broken.parse_command("  restart\tapi  ") == ("restart", "api", [])


def test_empty_command_is_rejected():
    with pytest.raises(ValueError, match="empty command"):
        broken.parse_command("   ")


def test_missing_target_is_rejected():
    with pytest.raises(ValueError, match="missing target"):
        broken.parse_command("deploy")


def test_describe_lists_arguments():
    assert broken.describe("scale  web  3  now") == "scale -> web with 3, now"


def test_targets_skips_bad_lines():
    assert broken.targets(["deploy  a", "oops", "stop   b"]) == ["a", "b"]
