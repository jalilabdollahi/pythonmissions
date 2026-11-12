import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import parse_line, parse_env_text


def test_simple_pair():
    assert parse_line("QUEUE=billing") == ("QUEUE", "billing")


def test_value_with_equals_signs():
    url = "postgres://u:p@db/app?sslmode=require&timeout=5"
    assert parse_line("DATABASE_URL=" + url) == ("DATABASE_URL", url), "only the first = separates key and value"


def test_base64_padding_is_kept():
    assert parse_line("TOKEN=YWJj==") == ("TOKEN", "YWJj==")


def test_whitespace_is_stripped():
    assert parse_line("  MODE = fast  ") == ("MODE", "fast")


def test_parse_text_skips_comments_and_blanks():
    text = "# batch\n\nQUEUE=billing\n  # more\nTOKEN=a=b\n"
    assert parse_env_text(text) == {"QUEUE": "billing", "TOKEN": "a=b"}


def test_empty_value_is_allowed():
    assert parse_env_text("EMPTY=\n") == {"EMPTY": ""}
