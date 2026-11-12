import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_long_value_keeps_only_last_four():
    assert broken.mask_value("abcdef123456") == "********3456", "keep the tail, never the head"


def test_short_values_are_fully_masked():
    assert broken.mask_value("hunter2") == "*******"
    assert broken.mask_value("12345678") == "********"
    assert broken.mask_value("") == ""


def test_key_name_and_separator_survive():
    assert broken.mask_line("login password: s3cretvalue99 ok") == "login password: *********ue99 ok"
    assert broken.mask_line("api_key=AKIA1234567890XYZ") == "api_key=*************0XYZ"


def test_key_names_are_case_insensitive():
    out = broken.mask_line("Token=abcdef123456 PASSWORD=zzzzzzzzzzzz")
    assert "abcdef123456" not in out and "zzzzzzzz" not in out


def test_every_secret_on_a_line_is_masked():
    line = "token=aaaaaaaaaaaa1111 secret=bbbbbbbbbbbb2222"
    out = broken.mask_line(line)
    assert out == "token=************1111 secret=************2222", "re.sub must replace all matches"


def test_bearer_header_is_masked():
    out = broken.mask_line("Authorization: Bearer eyJhbGciOiJIUzI1NiJ9")
    assert out == "Authorization: Bearer ****************NiJ9"


def test_lines_without_secrets_are_unchanged():
    line = "GET /health 200 12ms"
    assert broken.mask_line(line) == line


def test_mask_lines_and_leak_check():
    out = broken.mask_lines(["secret=abcdefghijkl", "ok"])
    assert out[1] == "ok"
    assert broken.leaked("\n".join(out), ["abcdefghijkl"]) == []
