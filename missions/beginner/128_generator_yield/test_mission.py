import os, sys, types
sys.path.insert(0, os.path.dirname(__file__))

def test_is_generator():
    from broken import config_stream
    result = config_stream({"host": "localhost"})
    assert hasattr(result, "__next__")

def test_yields_correct_content():
    from broken import config_stream
    result = list(config_stream({"host": "localhost", "port": "5432"}))
    assert "host=localhost" in result
    assert "port=5432" in result
