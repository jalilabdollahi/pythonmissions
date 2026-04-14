import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_equal_configs():
    from broken import Config
    c1 = Config({"host": "localhost", "port": 5432})
    c2 = Config({"host": "localhost", "port": 5432})
    assert c1 == c2

def test_unequal_configs():
    from broken import Config
    c1 = Config({"host": "localhost"})
    c2 = Config({"host": "remote"})
    assert c1 != c2
