import pytest
import sys
sys.path.insert(0, ".")
from broken import Scheduler

def test_run_once_all_services():
    s = Scheduler()
    s.register("api", lambda: "ok")
    s.register("db", lambda: "ok")
    s.run_once()
    assert "api" in s.results
    assert "db" in s.results

def test_run_until_immediate():
    import time
    s = Scheduler(interval=10)
    s.register("ping", lambda: "pong")
    s.run_until(0.05)
    assert "ping" in s.results
