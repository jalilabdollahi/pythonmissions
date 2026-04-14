import pytest
import sys
import threading
sys.path.insert(0, ".")
from broken import Counter

def test_increment():
    c = Counter()
    c.increment()
    c.increment()
    assert c.get() == 2

def test_decrement():
    c = Counter()
    c.increment()
    c.increment()
    c.decrement()
    assert c.get() == 1

def test_threaded_increment():
    c = Counter()
    threads = [threading.Thread(target=c.increment) for _ in range(100)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert c.get() == 100
