import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_kwargs():
    from broken import build_config
    cfg = build_config(host="localhost", port=5432)
    assert cfg == {"host": "localhost", "port": 5432}

def test_empty_call():
    from broken import build_config
    assert build_config() == {}

def test_single_kwarg():
    from broken import build_config
    assert build_config(debug=True) == {"debug": True}
