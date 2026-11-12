import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def make():
    h = broken.Headers()
    h.add("Content-Type", "application/json")
    h.add("Accept", "text/html")
    h.add("accept", " application/json ")
    h.add("X-Request-Id", "abc")
    return h


def test_lookup_ignores_case():
    h = make()
    assert h.get("content-type") == "application/json"
    assert h.get("CONTENT-TYPE") == "application/json", "names are case-insensitive"


def test_missing_header_returns_default():
    h = make()
    assert h.get("X-Nope") is None
    assert h.get("X-Nope", "-") == "-"


def test_repeated_headers_are_joined_with_comma():
    assert make().get("Accept") == "text/html, application/json"


def test_get_all_returns_every_value_stripped():
    assert make().get_all("ACCEPT") == ["text/html", "application/json"], "add() must append, not overwrite"
    assert make().get_all("Missing") == []


def test_membership_and_length():
    h = make()
    assert "x-request-id" in h
    assert "X-Other" not in h
    assert len(h) == 3


def test_items_keep_first_seen_spelling_and_order():
    assert make().items() == [
        ("Content-Type", "application/json"),
        ("Accept", "text/html, application/json"),
        ("X-Request-Id", "abc"),
    ]


def test_forward_lines_and_constructor_pairs():
    h = broken.Headers([("Host", "a.example"), ("host", "b.example")])
    assert broken.forward_lines(h) == ["Host: a.example, b.example"]
