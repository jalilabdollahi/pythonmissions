import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_digits_valid():
    from broken import is_valid_port_str
    assert is_valid_port_str("8080") is True

def test_letters_invalid():
    from broken import is_valid_port_str
    assert is_valid_port_str("abc") is False

def test_mixed_invalid():
    from broken import is_valid_port_str
    assert is_valid_port_str("80a") is False
