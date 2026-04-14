import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_string():
    from broken import encode_credentials
    assert isinstance(encode_credentials("admin", "pass"), str)

def test_correct_encoding():
    from broken import encode_credentials
    import base64
    expected = base64.b64encode(b"admin:pass").decode()
    assert encode_credentials("admin", "pass") == expected
