import os, sys
sys.path.insert(0, os.path.dirname(__file__))

def test_increments():
    import broken
    broken.COUNTER = 0
    broken.increment_counter()
    assert broken.get_counter() == 1

def test_increments_twice():
    import broken
    broken.COUNTER = 0
    broken.increment_counter()
    broken.increment_counter()
    assert broken.get_counter() == 2
