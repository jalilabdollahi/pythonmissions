import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_correct_count():
    from broken import all_combos
    result = all_combos(["prod","staging"],["web","api"],["us","eu"])
    assert len(result) == 8

def test_tuple_elements():
    from broken import all_combos
    result = all_combos(["prod"],["web"],["us"])
    assert result[0] == ("prod","web","us")
