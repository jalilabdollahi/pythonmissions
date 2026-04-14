import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_json_module():
    from broken import try_import_json
    j = try_import_json()
    assert hasattr(j, "dumps")
    assert hasattr(j, "loads")

def test_can_serialize():
    from broken import try_import_json
    j = try_import_json()
    assert j.dumps({"a": 1}) is not None
