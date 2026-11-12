import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_simple_pairs_and_comments():
    env = broken.parse_env("# comment\nA=1\n\nB=two\n")
    assert env == {"A": "1", "B": "two"}


def test_value_containing_equals_is_kept_whole():
    env = broken.parse_env("URL=postgres://h/db?sslmode=require&x=1\n")
    assert env["URL"] == "postgres://h/db?sslmode=require&x=1"


def test_base64_padding_equals_signs():
    assert broken.parse_env("KEY=YWJj==")["KEY"] == "YWJj=="


def test_export_prefix_is_ignored():
    env = broken.parse_env("export TOKEN=abc\nexport   OTHER=2")
    assert env == {"TOKEN": "abc", "OTHER": "2"}


def test_double_and_single_quotes_removed():
    env = broken.parse_env("PW=\"s3 cret\"\nNAME='bob'\n")
    assert env == {"PW": "s3 cret", "NAME": "bob"}


def test_hash_inside_quotes_is_data():
    assert broken.parse_env('COLOR="#ff0000"')["COLOR"] == "#ff0000"


def test_mismatched_quote_is_left_alone():
    assert broken.parse_env("Q='abc\"")["Q"] == "'abc\""


def test_lines_without_equals_ignored_and_file_load(tmp_path):
    p = tmp_path / ".env"
    p.write_text("junk line\nA=1\n")
    assert broken.load_env_file(str(p)) == {"A": "1"}
