import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_lowercases_and_strips():
    assert broken.sanitize_hostname("  WebServer ") == "webserver"


def test_underscores_become_hyphens():
    assert broken.sanitize_hostname("api_gateway") == "api-gateway", "replace() returns a new string"


def test_inner_spaces_are_removed():
    assert broken.sanitize_hostname("db 01") == "db01"


def test_fqdn_joins_zone():
    assert broken.fqdn("Web_Server 01", "corp.example") == "web-server01.corp.example"


def test_sanitize_all_deduplicates_in_order():
    assert broken.sanitize_all(["A_b", "a-b", "C"]) == ["a-b", "c"]


def test_invalid_names_after_cleanup():
    assert broken.invalid_names(["ok_name", "bad!name"]) == ["bad!name"]
