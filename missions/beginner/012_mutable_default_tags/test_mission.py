import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import tag_resource, standard_tags


def test_first_call_returns_one_tag():
    assert tag_resource("db", "env:prod") == ["env:prod"]


def test_second_call_does_not_inherit_tags():
    tag_resource("db", "env:prod")
    assert tag_resource("bucket", "env:test") == ["env:test"], "tags must not leak between calls"


def test_passed_list_is_extended():
    existing = ["a"]
    assert tag_resource("db", "b", existing) == ["a", "b"]


def test_standard_tags_are_repeatable():
    assert standard_tags("payments") == ["owner:payments", "managed:true"]
    assert standard_tags("risk") == ["owner:risk", "managed:true"]


def test_results_are_independent_lists():
    first = tag_resource("x", "one")
    second = tag_resource("y", "two")
    assert first is not second
