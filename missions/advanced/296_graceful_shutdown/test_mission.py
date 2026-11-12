import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Server


def make(grace=30):
    clock = {"now": 0}
    return Server(lambda: clock["now"], grace), clock


def slow(clock, seconds):
    def job():
        clock["now"] += seconds

    return job


def test_clean_drain_runs_everything_and_exits_zero():
    server, clock = make()
    for name in "abc":
        server.submit(name, slow(clock, 1))
    assert server.drain() == 0
    assert server.report()["done"] == ["a", "b", "c"]


def test_signal_stops_accepting_new_work_immediately():
    server, _ = make()
    assert server.submit("before", lambda: None)
    assert server.handle_signal() == "draining"
    assert server.submit("after", lambda: None) is False
    assert server.report()["rejected"] == ["after"]


def test_jobs_cannot_enqueue_follow_up_work_while_draining():
    server, _ = make()
    server.submit("parent", lambda: server.submit("child", lambda: None))
    server.handle_signal()
    server.drain()
    assert server.report()["done"] == ["parent"]
    assert server.report()["rejected"] == ["child"]


def test_failing_job_does_not_stop_the_drain():
    server, _ = make()

    def boom():
        raise RuntimeError("bad job")

    server.submit("bad", boom)
    server.submit("good", lambda: None)
    assert server.drain() == 1, "a failed job makes the exit code non-zero"
    assert server.report()["failed"] == ["bad"]
    assert server.report()["done"] == ["good"], "the queue behind the failure still drains"


def test_deadline_abandons_the_remaining_jobs():
    server, clock = make(grace=30)
    for name in ["j1", "j2", "j3", "j4", "j5"]:
        server.submit(name, slow(clock, 10))
    assert server.drain() == 1
    assert server.report()["done"] == ["j1", "j2", "j3"]
    assert server.report()["abandoned"] == ["j4", "j5"], "stop at the deadline and report the leftovers"


def test_second_signal_forces_immediate_exit():
    server, clock = make(grace=300)

    def impatient_operator():
        clock["now"] += 1
        assert server.handle_signal() == "force"

    server.submit("first", impatient_operator)
    server.submit("second", lambda: None)
    server.handle_signal()
    assert server.drain() == 1
    assert server.report()["done"] == ["first"]
    assert server.report()["abandoned"] == ["second"]
