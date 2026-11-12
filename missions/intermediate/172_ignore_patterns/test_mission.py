import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


RULES = ["# build output", "build/", "*.bak", "Thumbs.db", "secrets/*", "!secrets/public.pem", "", "node_modules/"]


def test_extension_pattern_matches_in_subfolders():
    assert broken.is_ignored("deploy/app.bak", RULES), "patterns without '/' apply to the file name at any depth"


def test_plain_name_pattern_matches_at_any_depth():
    assert broken.is_ignored("assets/img/Thumbs.db", RULES), "a bare name is compared with the file name, not the whole path"
    assert broken.is_ignored("Thumbs.db", RULES)


def test_extension_pattern_matches_top_level():
    assert broken.is_ignored("old.bak", RULES)


def test_directory_pattern_matches_nested_directories():
    assert broken.is_ignored("docs/build/index.html", RULES)
    assert broken.is_ignored("build/out.js", RULES)


def test_directory_pattern_does_not_match_similar_names():
    assert not broken.is_ignored("rebuild/out.js", RULES)
    assert not broken.is_ignored("src/builder.py", RULES)


def test_negation_rescues_a_file_when_it_comes_last():
    assert broken.is_ignored("secrets/private.pem", RULES)
    assert not broken.is_ignored("secrets/public.pem", RULES), "the last matching line wins, and '!' un-ignores"


def test_later_pattern_can_ignore_again():
    rules = ["!keep.txt", "*.txt"]
    assert broken.is_ignored("keep.txt", rules)


def test_comments_and_blank_lines_are_skipped():
    assert not broken.is_ignored("README.md", ["# README.md", "   ", ""])


def test_filter_paths_keeps_order():
    paths = ["a.py", "x.bak", "node_modules/z/index.js", "b.py"]
    assert broken.filter_paths(paths, RULES) == ["a.py", "b.py"]
