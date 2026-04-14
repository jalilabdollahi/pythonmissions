import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_all_pairs():
    from broken import merge_env_configs
    result = merge_env_configs(["prod","staging","dev"], [{"d":False},{"d":True}])
    assert len(result) == 3

def test_missing_filled():
    from broken import merge_env_configs
    result = merge_env_configs(["prod","staging","dev"], [{"d":False},{"d":True}])
    assert result[2][1] == {}
