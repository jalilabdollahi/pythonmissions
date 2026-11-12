import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def double(x):
    return x * 2


def test_results_are_in_payload_order():
    out = broken.run_jobs(list(range(10)), double, workers=4, join_timeout=0.5)
    assert out["results"] == [x * 2 for x in range(10)]
    assert out["errors"] == {}


def test_all_workers_stop_after_the_work_is_done():
    out = broken.run_jobs(list(range(6)), double, workers=3, join_timeout=0.3)
    assert out["stopped"] is True, "each worker needs its own sentinel to leave q.get()"


def test_every_queue_item_is_acknowledged():
    out = broken.run_jobs(list(range(6)), double, workers=3, join_timeout=0.3)
    assert out["unfinished"] == 0, "call task_done() for every get(), sentinels included"


def test_handler_errors_are_recorded_and_do_not_kill_the_pool():
    def handler(x):
        if x == 2:
            raise ValueError("corrupt image")
        return x

    out = broken.run_jobs(list(range(8)), handler, workers=1, join_timeout=0.5)
    assert out["results"] == [0, 1, 3, 4, 5, 6, 7], "a failing job must not stop the worker"
    assert out["errors"] == {2: "ValueError('corrupt image')"}
    assert out["stopped"] is True
    assert out["unfinished"] == 0


def test_no_payloads_still_shuts_down():
    out = broken.run_jobs([], double, workers=2, join_timeout=0.3)
    assert out == {"results": [], "errors": {}, "stopped": True, "unfinished": 0}


def test_more_workers_than_jobs():
    out = broken.run_jobs([5], double, workers=5, join_timeout=0.3)
    assert out["results"] == [10]
    assert out["stopped"] is True
