import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_parses_dict():
    from broken import parse_response
    result = parse_response('{"status": "ok", "code": 200}')
    assert result == {"status": "ok", "code": 200}

def test_parses_list():
    from broken import parse_response
    result = parse_response('[1, 2, 3]')
    assert result == [1, 2, 3]
