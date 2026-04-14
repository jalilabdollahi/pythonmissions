import pytest, sys
sys.path.insert(0, ".")
from broken import RestClient
from unittest.mock import MagicMock

def make_resp(status):
    r = MagicMock()
    r.status_code = status
    return r

def test_success():
    sess = MagicMock()
    sess.get.return_value = make_resp(200)
    client = RestClient(sess)
    r = client.get("http://example.com")
    assert r.status_code == 200

def test_404_not_retried():
    sess = MagicMock()
    sess.get.return_value = make_resp(404)
    client = RestClient(sess)
    r = client.get("http://example.com")
    assert r.status_code == 404
    assert sess.get.call_count == 1

def test_500_retried():
    sess = MagicMock()
    sess.get.return_value = make_resp(500)
    client = RestClient(sess, max_retries=2)
    with pytest.raises(ValueError):
        client.get("http://example.com")
    assert sess.get.call_count == 2
