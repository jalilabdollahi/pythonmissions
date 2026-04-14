import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_dict():
    from broken import health_check
    result = health_check("localhost", 8080)
    assert isinstance(result, dict)

def test_healthy():
    from broken import health_check
    result = health_check("localhost", 8080)
    assert result["healthy"] is True

def test_unhealthy_bad_port():
    from broken import health_check
    result = health_check("localhost", 0)
    assert result["healthy"] is False

def test_return_annotation():
    from broken import health_check
    assert health_check.__annotations__["return"] == dict
