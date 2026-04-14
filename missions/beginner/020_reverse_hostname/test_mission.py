import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_reverses():
    from broken import reverse_host
    assert reverse_host("web.internal.net") == "ten.lanretni.bew"

def test_palindrome():
    from broken import reverse_host
    assert reverse_host("abcba") == "abcba"

def test_single_char():
    from broken import reverse_host
    assert reverse_host("x") == "x"
