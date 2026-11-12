import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


import threading
import time


def test_results_follow_input_order_even_if_probes_finish_out_of_order():
    gate = threading.Event()

    def probe(host):
        if host == "r1":
            assert gate.wait(timeout=2), "r1 waits for r3"
        if host == "r3":
            gate.set()
        return host.upper()

    out = broken.probe_all(["r1", "r2", "r3"], probe, workers=3)
    assert [r["host"] for r in out] == ["r1", "r2", "r3"], "keep futures in submission order"
    assert [r["value"] for r in out] == ["R1", "R2", "R3"]


def test_successful_probe_shape():
    out = broken.probe_all(["a"], lambda h: 42)
    assert out == [{"host": "a", "ok": True, "value": 42}]


def test_probe_exception_is_recorded_not_raised():
    def probe(host):
        if host == "bad":
            raise ValueError("no route")
        return "up"

    out = broken.probe_all(["x", "bad", "y"], probe)
    assert out[1] == {"host": "bad", "ok": False, "error": "ValueError: no route"}
    assert out[0]["ok"] and out[2]["ok"], "one failure must not abort the others"


def test_failed_hosts_lists_only_failures_in_order():
    def probe(host):
        if host in ("b", "d"):
            raise OSError("down")
        return 1

    out = broken.probe_all(["a", "b", "c", "d"], probe)
    assert broken.failed_hosts(out) == ["b", "d"]
    assert broken.failed_hosts([]) == []


def test_worker_limit_is_respected():
    lock = threading.Lock()
    state = {"active": 0, "peak": 0}

    def probe(host):
        with lock:
            state["active"] += 1
            state["peak"] = max(state["peak"], state["active"])
        time.sleep(0.02)
        with lock:
            state["active"] -= 1
        return host

    broken.probe_all(["h%d" % i for i in range(8)], probe, workers=2)
    assert state["peak"] <= 2, "max_workers must be passed to the executor"


def test_empty_host_list():
    assert broken.probe_all([], lambda h: h) == []
