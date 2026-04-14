import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_https_is_secure():
    from broken import is_secure
    assert is_secure("https://api.internal/health") is True

def test_http_is_not_secure():
    from broken import is_secure
    assert is_secure("http://api.internal/health") is False

def test_ftp_is_not_secure():
    from broken import is_secure
    assert is_secure("ftp://files.internal") is False
