import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_returns_list():
    from broken import top_errors
    assert isinstance(top_errors([500, 404, 500], 2), list)

def test_most_common_first():
    from broken import top_errors
    codes = [500, 404, 500, 503, 500, 404, 200, 503, 500]
    result = top_errors(codes, 1)
    assert result[0][0] == 500

def test_correct_count():
    from broken import top_errors
    result = top_errors([500, 500, 404], 1)
    assert result[0][1] == 2

def test_n_limits_results():
    from broken import top_errors
    result = top_errors([500, 404, 503, 200], 2)
    assert len(result) == 2
