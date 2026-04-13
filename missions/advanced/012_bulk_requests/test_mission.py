import os
import sys
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(__file__))


def make_mock_response(status_code):
    m = MagicMock()
    m.status_code = status_code
    return m


URLS = [
    "http://svc1.internal/health",
    "http://svc2.internal/health",
    "http://svc3.internal/health",
    "http://svc4.internal/health",
]


def test_returns_list():
    from broken import check_urls_concurrent
    responses = [make_mock_response(200)] * len(URLS)
    with patch("broken.requests.get", side_effect=responses):
        result = check_urls_concurrent(URLS)
    assert isinstance(result, list)


def test_returns_correct_count():
    from broken import check_urls_concurrent
    responses = [make_mock_response(200)] * len(URLS)
    with patch("broken.requests.get", side_effect=responses):
        result = check_urls_concurrent(URLS)
    assert len(result) == len(URLS)


def test_all_urls_checked():
    from broken import check_urls_concurrent
    checked = []

    def fake_get(url, timeout=5):
        checked.append(url)
        return make_mock_response(200)

    with patch("broken.requests.get", side_effect=fake_get):
        check_urls_concurrent(URLS)

    assert len(checked) == len(URLS)


def test_healthy_marked_correctly():
    from broken import check_urls_concurrent
    responses = [make_mock_response(200), make_mock_response(503), make_mock_response(200), make_mock_response(200)]
    with patch("broken.requests.get", side_effect=responses):
        results = check_urls_concurrent(URLS)

    healthy = [r for r in results if r["healthy"]]
    unhealthy = [r for r in results if not r["healthy"]]
    assert len(healthy) == 3
    assert len(unhealthy) == 1


def test_summarize_results():
    from broken import summarize_results
    results = [
        {"url": "a", "healthy": True},
        {"url": "b", "healthy": False},
        {"url": "c", "healthy": True},
    ]
    summary = summarize_results(results)
    assert summary["total"] == 3
    assert summary["healthy"] == 2
    assert summary["unhealthy"] == 1
    assert "b" in summary["unhealthy_urls"]
