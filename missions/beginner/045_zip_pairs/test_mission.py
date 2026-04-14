import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_all_pairs():
    from broken import pair_services
    result = pair_services(["web-01", "api-01", "db-01"], [80, 8080, 5432])
    assert len(result) == 3

def test_correct_pairing():
    from broken import pair_services
    result = pair_services(["web-01", "db-01"], [80, 5432])
    assert result[0] == ("web-01", 80)
    assert result[1] == ("db-01", 5432)
