import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_replaces_hostname():
    from broken import swap_host
    assert swap_host("host=server-01.internal", "server-01", "server-02") == "host=server-02.internal"

def test_no_match():
    from broken import swap_host
    assert swap_host("host=server-01.internal", "server-03", "server-04") == "host=server-01.internal"

def test_multiple_occurrences():
    from broken import swap_host
    assert swap_host("a=old,b=old", "old", "new") == "a=new,b=new"
