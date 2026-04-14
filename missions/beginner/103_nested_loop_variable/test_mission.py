import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_correct_count():
    from broken import config_pairs
    result = config_pairs(["prod","staging"], ["web","api"])
    assert len(result) == 4

def test_correct_pairs():
    from broken import config_pairs
    result = config_pairs(["prod"], ["web","api"])
    assert ("prod", "web") in result
    assert ("prod", "api") in result

def test_no_same_env_svc():
    from broken import config_pairs
    result = config_pairs(["prod","staging"], ["web","api"])
    assert all(pair[0] != pair[1] for pair in result)
