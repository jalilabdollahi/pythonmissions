import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import build_url, sweep_urls


def test_build_url_returns_the_url():
    assert build_url("a.example.com", "metrics") == "https://a.example.com/metrics", "the URL must be returned, not printed"


def test_parameters_are_encoded():
    url = build_url("a.example.com", "metrics", {"job": "web api", "fmt": "json"})
    assert url == "https://a.example.com/metrics?job=web+api&fmt=json"


def test_leading_slash_in_path_does_not_double():
    assert build_url("b.example.com", "/v1/health") == "https://b.example.com/v1/health"


def test_sweep_builds_one_url_per_host():
    urls = sweep_urls(["x.io", "y.io"], "/stats")
    assert urls == ["https://x.io/stats?format=json", "https://y.io/stats?format=json"]


def test_nothing_is_printed(capsys):
    build_url("quiet.example.com", "ping")
    assert capsys.readouterr().out == "", "helpers should not print"
