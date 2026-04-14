import pytest
import sys
sys.path.insert(0, ".")
from broken import check_endpoint, check_all
from unittest.mock import MagicMock

def make_response(status):
    r = MagicMock()
    r.status_code = status
    return r

def test_200_healthy():
    session = MagicMock()
    session.get.return_value = make_response(200)
    assert check_endpoint("http://example.com/health", session) is True

def test_201_healthy():
    session = MagicMock()
    session.get.return_value = make_response(201)
    assert check_endpoint("http://example.com/resource", session) is True

def test_500_unhealthy():
    session = MagicMock()
    session.get.return_value = make_response(500)
    assert check_endpoint("http://example.com/health", session) is False
