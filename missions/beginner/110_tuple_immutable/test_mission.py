import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_tuple():
    from broken import add_to_config
    result = add_to_config(("a", "b"), "c")
    assert isinstance(result, tuple)

def test_item_added():
    from broken import add_to_config
    result = add_to_config(("a", "b"), "c")
    assert "c" in result

def test_original_preserved():
    from broken import add_to_config
    original = ("host=localhost",)
    add_to_config(original, "port=5432")
    assert len(original) == 1
