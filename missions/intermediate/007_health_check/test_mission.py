import os
import sys
from unittest.mock import MagicMock, patch

import requests as req

sys.path.insert(0, os.path.dirname(__file__))


def make_mock_response(status_code=200):
    mock = MagicMock()
    mock.status_code = status_code
    return mock


def test_healthy_endpoint():
    from broken import check_endpoint
    with patch("broken.requests.get", return_value=make_mock_response(200)):
        result = check_endpoint("http://example.com/health")
    assert result["healthy"] is True
    assert result["status_code"] == 200
    assert result["error"] is None


def test_unhealthy_500():
    from broken import check_endpoint
    with patch("broken.requests.get", return_value=make_mock_response(500)):
        result = check_endpoint("http://example.com/health")
    assert result["healthy"] is False
    assert result["status_code"] == 500


def test_unhealthy_404():
    from broken import check_endpoint
    with patch("broken.requests.get", return_value=make_mock_response(404)):
        result = check_endpoint("http://example.com/health")
    assert result["healthy"] is False


def test_request_exception_handled():
    from broken import check_endpoint
    with patch("broken.requests.get", side_effect=req.exceptions.ConnectionError("refused")):
        result = check_endpoint("http://down.internal")
    assert result["healthy"] is False
    assert result["error"] is not None


def test_timeout_is_passed():
    from broken import check_endpoint
    with patch("broken.requests.get", return_value=make_mock_response(200)) as mock_get:
        check_endpoint("http://example.com")
        call_kwargs = mock_get.call_args
        kwargs = call_kwargs[1] if call_kwargs[1] else {}
        args = call_kwargs[0] if call_kwargs[0] else ()
        has_timeout = "timeout" in kwargs or len(args) > 1
        assert has_timeout


def test_check_all_summary():
    from broken import check_all
    responses = [make_mock_response(200), make_mock_response(503)]
    with patch("broken.requests.get", side_effect=responses):
        summary = check_all(["http://up.com", "http://down.com"])
    assert summary["total"] == 2
    assert summary["healthy"] == 1
    assert summary["unhealthy"] == 1
