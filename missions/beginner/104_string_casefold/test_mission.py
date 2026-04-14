import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_basic_case():
    from broken import same_user
    assert same_user("Admin", "admin") is True

def test_all_caps():
    from broken import same_user
    assert same_user("ADMIN", "admin") is True

def test_unicode_casefold():
    from broken import normalize_user
    assert normalize_user("stra\u00dfe") == "strasse"
