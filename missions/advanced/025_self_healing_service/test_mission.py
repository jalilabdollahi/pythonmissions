import pytest, sys
sys.path.insert(0, ".")
from broken import SelfHealingManager, ManagedService

def test_heals_failed():
    mgr = SelfHealingManager(base_delay=0)
    calls = []
    svc = ManagedService("api", lambda: calls.append(1))
    svc.state = "failed"
    mgr.register(svc)
    states = mgr.heal()
    assert states["api"] == "running"

def test_ignores_running():
    mgr = SelfHealingManager(base_delay=0)
    started = []
    svc = ManagedService("db", lambda: started.append(1))
    svc.state = "running"
    mgr.register(svc)
    mgr.heal()
    assert len(started) == 0

def test_exponential_backoff():
    mgr = SelfHealingManager(base_delay=1.0)
    svc = ManagedService("worker", lambda: None)
    svc.restart_count = 0
    d0 = mgr._backoff_delay(svc)
    svc.restart_count = 1
    d1 = mgr._backoff_delay(svc)
    svc.restart_count = 2
    d2 = mgr._backoff_delay(svc)
    assert d1 == d0 * 2
    assert d2 == d0 * 4
