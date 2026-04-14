import os, sys, json, tempfile
sys.path.insert(0, os.path.dirname(__file__))

def test_missing_file_returns_empty():
    from broken import load_config
    assert load_config("/nonexistent/path/config.json") == {}

def test_valid_file():
    from broken import load_config
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump({"host": "localhost"}, f)
        name = f.name
    assert load_config(name) == {"host": "localhost"}
