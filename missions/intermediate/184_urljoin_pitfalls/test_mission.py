import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


BASE = "https://api.tidewater.example/v2"


def test_base_without_trailing_slash_keeps_its_path():
    assert broken.join_url(BASE, "claims/17") == "https://api.tidewater.example/v2/claims/17"


def test_base_with_trailing_slash_gives_same_result():
    assert broken.join_url(BASE + "/", "claims/17") == "https://api.tidewater.example/v2/claims/17"


def test_leading_slash_in_path_does_not_reset_to_root():
    assert broken.join_url(BASE, "/claims") == "https://api.tidewater.example/v2/claims", \
        "urljoin treats '/claims' as an absolute path on the host"


def test_nested_base_path():
    assert broken.join_url("http://h/a/b/c", "x") == "http://h/a/b/c/x"


def test_query_values_are_url_encoded():
    url = broken.with_query("http://h/search", {"q": "a b&c=d"})
    assert url == "http://h/search?q=a+b%26c%3Dd", "use urlencode so '&' and '=' cannot inject parameters"


def test_query_params_are_sorted_and_existing_query_kept():
    url = broken.with_query("http://h/s?page=2#top", {"z": 1, "a": 2})
    assert url == "http://h/s?page=2&a=2&z=1#top"


def test_endpoint_combines_join_and_query():
    assert broken.endpoint(BASE, "/claims", status="open") == "https://api.tidewater.example/v2/claims?status=open"
    assert broken.endpoint(BASE, "claims") == "https://api.tidewater.example/v2/claims"


def test_api_urls():
    assert broken.api_urls("http://h/v1", ["a", "/b"]) == ["http://h/v1/a", "http://h/v1/b"]
