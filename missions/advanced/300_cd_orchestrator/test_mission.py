import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import (
    ApprovalBook,
    CycleError,
    FakeDeployer,
    IllegalTransition,
    Orchestrator,
    ServiceRun,
    plan_order,
)

DEPENDS = {"api": ["db", "cache"], "web": ["api"]}
OLD = {"db": "1.0", "cache": "1.0", "api": "1.0", "web": "1.0"}
NEW = {"db": "2.0", "cache": "2.0", "api": "2.0", "web": "2.0"}


def build(deployer=None, approvals_needed=2, current=None):
    clock = {"now": 1000}
    book = ApprovalBook(lambda: clock["now"], required=approvals_needed, ttl=600)
    deployer = deployer or FakeDeployer()
    orch = Orchestrator(
        deployer, DEPENDS, current or {"staging": dict(OLD), "prod": dict(OLD)}, book
    )
    return orch, deployer, book, clock


def approve(book, release="r1"):
    book.approve(release, "alice")
    book.approve(release, "bob")


def test_dependencies_deploy_before_dependents():
    assert plan_order(NEW, DEPENDS) == ["cache", "db", "api", "web"]


def test_dependency_outside_the_release_counts_as_already_deployed():
    assert plan_order({"api": "2.0", "web": "2.0"}, DEPENDS) == ["api", "web"]


def test_real_cycles_are_rejected():
    try:
        plan_order({"a": "1", "b": "1"}, {"a": ["b"], "b": ["a"]})
    except CycleError:
        return
    raise AssertionError("a dependency cycle must raise CycleError")


def test_approvals_need_distinct_non_author_unexpired_reviewers():
    clock = {"now": 0}
    book = ApprovalBook(lambda: clock["now"], required=2, ttl=100)
    book.approve("r1", "alice")
    book.approve("r1", "alice")
    assert not book.is_approved("r1", "zed"), "one reviewer approving twice is one approval"
    book.approve("r1", "zed")
    assert not book.is_approved("r1", "zed"), "the author cannot approve their own release"
    book.approve("r1", "bob")
    assert book.is_approved("r1", "zed")
    clock["now"] = 500
    assert not book.is_approved("r1", "zed"), "stale approvals expire"


def test_prod_waits_for_approval_but_staging_goes_ahead():
    orch, deployer, book, _ = build()
    report = orch.release("r1", "zed", NEW)
    assert report["status"] == "awaiting_approval" and report["blocked_at"] == "prod"
    assert report["stages"] == {"staging": "live"}
    assert not any(call[1] == "prod" for call in deployer.calls), "nothing may touch prod yet"
    assert orch.current["staging"] == NEW and orch.current["prod"] == OLD


def test_approved_release_reaches_prod_in_dependency_order():
    orch, deployer, book, _ = build()
    approve(book)
    report = orch.release("r1", "zed", NEW)
    assert report["status"] == "succeeded"
    prod_calls = [c[2] for c in deployer.calls if c[0] == "deploy" and c[1] == "prod"]
    assert prod_calls == ["cache", "db", "api", "web"]
    assert orch.states("prod") == {s: "live" for s in NEW}
    assert orch.current["prod"] == NEW


def test_failed_health_check_rolls_back_everything_started_newest_first():
    deployer = FakeDeployer(unhealthy={("prod", "api", "2.0")})
    orch, deployer, book, _ = build(deployer)
    approve(book)
    report = orch.release("r1", "zed", NEW)
    assert report["status"] == "rolled_back"
    rollbacks = [c[2:] for c in deployer.calls[-3:]]
    assert rollbacks == [("api", "1.0"), ("db", "1.0"), ("cache", "1.0")], "reverse order, failed one first"
    assert deployer.live[("prod", "api")] == "1.0", "the failed service must not stay on 2.0"
    assert orch.states("prod") == {"cache": "rolled_back", "db": "rolled_back", "api": "rolled_back"}
    assert orch.current["staging"] == NEW, "staging finished live and keeps its new versions"


def test_failed_release_does_not_change_what_is_recorded_as_deployed():
    deployer = FakeDeployer(unhealthy={("prod", "web", "2.0"), ("prod", "web", "3.0")})
    orch, deployer, book, _ = build(deployer)
    approve(book, "r1")
    orch.release("r1", "zed", NEW)
    assert orch.current["prod"] == OLD, "a rolled back stage must not be recorded as deployed"
    approve(book, "r2")
    orch.release("r2", "zed", {s: "3.0" for s in NEW})
    last = [c for c in deployer.calls if c[1] == "prod"][-4:]
    assert {c[3] for c in last if c[0] == "deploy"} >= {"1.0"}, "second rollback targets the last good version"
    assert deployer.live[("prod", "web")] == "1.0"


def test_new_services_are_removed_and_broken_rollbacks_do_not_stop_the_rest():
    current = {"staging": {"db": "1.0"}, "prod": {"db": "1.0"}}
    deployer = FakeDeployer(unhealthy={("prod", "web", "2.0")}, fail_deploy={("prod", "db", "1.0")})
    orch, deployer, book, _ = build(deployer, current=current)
    approve(book)
    report = orch.release("r1", "zed", {"db": "2.0", "api": "2.0", "web": "2.0"})
    assert report["status"] == "rollback_incomplete"
    assert ("remove", "prod", "web") in deployer.calls and ("remove", "prod", "api") in deployer.calls
    assert orch.states("prod") == {"db": "rollback_failed", "api": "rolled_back", "web": "rolled_back"}


def test_state_machine_forbids_skipping_verification():
    run = ServiceRun("api")
    run.move("deploying")
    try:
        run.move("live")
    except IllegalTransition:
        return
    raise AssertionError("deploying -> live must be illegal")
