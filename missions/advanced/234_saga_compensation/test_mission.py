import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import FakeCloud, Step, preview_environment, run_saga


def test_happy_path_leaves_everything_in_place():
    cloud = FakeCloud()
    result = run_saga(preview_environment(cloud), {})
    assert result["status"] == "completed"
    assert result["completed"] == ["network", "database", "dns", "deploy"]
    assert len(cloud.resources) == 4


def test_failure_rolls_back_everything_that_was_created():
    cloud = FakeCloud(fail_on="deploy")
    result = run_saga(preview_environment(cloud), {})
    assert result["status"] == "rolled_back"
    assert result["failure"] == ("deploy", "quota exceeded creating deploy")
    assert cloud.resources == {}, "no orphaned resources may remain"


def test_only_completed_steps_are_compensated():
    cloud = FakeCloud(fail_on="dns")
    result = run_saga(preview_environment(cloud), {})
    assert result["completed"] == ["network", "database"], "dns raised, it never completed"
    assert result["compensated"] == ["database", "network"]
    assert result["compensation_errors"] == []


def test_compensation_runs_in_reverse_order_of_creation():
    cloud = FakeCloud(fail_on="deploy")
    run_saga(preview_environment(cloud), {})
    deletes = [handle for op, handle in cloud.calls if op == "delete"]
    assert deletes == ["dns-3", "database-2", "network-1"], "children before parents"


def test_each_compensation_gets_its_own_steps_result():
    seen = []
    steps = [
        Step("a", lambda ctx: "handle-a", lambda r: seen.append(("a", r))),
        Step("b", lambda ctx: "handle-b", lambda r: seen.append(("b", r))),
        Step("c", lambda ctx: 1 / 0, lambda r: seen.append(("c", r))),
    ]
    run_saga(steps, {})
    assert seen == [("b", "handle-b"), ("a", "handle-a")]


def test_a_failing_compensation_does_not_stop_the_rest():
    cloud = FakeCloud(fail_on="deploy", fail_delete={"dns"})
    result = run_saga(preview_environment(cloud), {})
    assert result["status"] == "rollback_incomplete"
    assert result["compensation_errors"] == [("dns", "cannot delete dns right now")]
    assert result["compensated"] == ["database", "network"]
    assert sorted(cloud.resources.values()) == ["dns"], "only the stuck resource is left over"


def test_first_step_failure_has_nothing_to_undo():
    cloud = FakeCloud(fail_on="network")
    result = run_saga(preview_environment(cloud), {})
    assert result["completed"] == [] and result["compensated"] == []
    assert [op for op, _ in cloud.calls] == ["create"]
