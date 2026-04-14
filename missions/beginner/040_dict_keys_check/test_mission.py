import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_all_present():
    from broken import has_required_keys
    assert has_required_keys({"host": "x", "port": 5432}, ["host", "port"]) is True

def test_missing_key():
    from broken import has_required_keys
    assert has_required_keys({"host": "x"}, ["host", "port"]) is False

def test_empty_required():
    from broken import has_required_keys
    assert has_required_keys({}, []) is True

def test_empty_cfg():
    from broken import has_required_keys
    assert has_required_keys({}, ["host"]) is False
