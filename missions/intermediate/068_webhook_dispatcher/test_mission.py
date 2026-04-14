import pytest, sys
sys.path.insert(0, ".")
from broken import dispatch_webhook
from unittest.mock import MagicMock

def test_success():
    sess = MagicMock()
    resp = MagicMock()
    resp.ok = True
    resp.status_code = 200
    sess.post.return_value = resp
    result = dispatch_webhook("http://hooks.example.com", {"type": "deploy"}, sess)
    assert result["success"] is True
    call_kwargs = sess.post.call_args[1]
    assert "json" in call_kwargs

def test_failure():
    sess = MagicMock()
    resp = MagicMock()
    resp.ok = False
    resp.status_code = 500
    sess.post.return_value = resp
    result = dispatch_webhook("http://hooks.example.com", {"type": "deploy"}, sess)
    assert result["success"] is False
