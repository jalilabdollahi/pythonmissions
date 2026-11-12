import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

SAMPLES = [
    ("/login", 100), ("/login", 140),
    ("/search", 480), ("/search", 520), ("/search", 500),
    ("/health", 4),
    ("/export", 900),
    ("/profile", 60), ("/profile", 80),
]


def test_average_uses_per_endpoint_sample_count():
    avgs = broken.average_latencies(SAMPLES)
    assert avgs["/login"] == 120
    assert avgs["/search"] == 500
    assert avgs["/export"] == 900


def test_keeps_the_slowest_not_the_fastest():
    names = [name for name, _ in broken.slowest_endpoints(SAMPLES, 2)]
    assert sorted(names) == ["/export", "/search"], "a min-heap evicts its smallest element, which is the fastest of the winners"


def test_results_are_slowest_first():
    rows = broken.slowest_endpoints(SAMPLES, 3)
    assert rows == [("/export", 900), ("/search", 500), ("/login", 120)]


def test_k_larger_than_endpoint_count_returns_everything():
    assert len(broken.slowest_endpoints(SAMPLES, 50)) == 5


def test_k_zero_returns_nothing():
    assert broken.slowest_endpoints(SAMPLES, 0) == []


def test_worst_endpoint_and_empty_board():
    assert broken.worst_endpoint(SAMPLES) == "/export"
    assert broken.worst_endpoint([]) is None
    assert broken.format_board([]) == "(no data)"


def test_breaching_lists_endpoints_over_the_limit():
    assert broken.breaching(SAMPLES, 400) == ["/export", "/search"]


def test_board_text():
    rows = broken.slowest_endpoints([("/a", 10), ("/b", 30)], 2)
    assert broken.format_board(rows).splitlines() == [
        "1. /b                 30.0 ms",
        "2. /a                 10.0 ms",
    ]
