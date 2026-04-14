import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_sums_correctly():
    from broken import total_ms
    assert total_ms(["120", "340", "89", "456"]) == 1005

def test_single_item():
    from broken import total_ms
    assert total_ms(["500"]) == 500

def test_all_zeros():
    from broken import total_ms
    assert total_ms(["0", "0", "0"]) == 0
