import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_three_tags():
    from broken import tags_to_list
    assert tags_to_list("web,api,db") == ["web", "api", "db"]

def test_single_tag():
    from broken import tags_to_list
    assert tags_to_list("web") == ["web"]

def test_strips_spaces():
    from broken import tags_to_list
    assert tags_to_list("web, api, db") == ["web", "api", "db"]
