import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_all_even():
    from broken import even_ports
    result = even_ports(8000, 8010)
    assert all(p % 2 == 0 for p in result)

def test_correct_count():
    from broken import even_ports
    assert len(even_ports(8000, 8010)) == 5

def test_starts_at_start():
    from broken import even_ports
    assert even_ports(8000, 8010)[0] == 8000
