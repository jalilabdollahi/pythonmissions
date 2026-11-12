import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import describe, has_drift, plan, summary


def res(type_, managed=True, **props):
    return {"type": type_, "props": props, "managed_by": "kestrel" if managed else "someone-else"}


def want(type_, **props):
    return {"type": type_, "props": props}


def ops(actions):
    return [(a["op"], a["name"]) for a in actions]


def test_matching_state_has_no_drift():
    desired = {"api": want("service", replicas=3)}
    actual = {"api": res("service", replicas=3)}
    assert plan(desired, actual) == []
    assert not has_drift(desired, actual)


def test_missing_resources_are_created():
    assert ops(plan({"cache": want("redis", size=2)}, {})) == [("create", "cache")]


def test_unmanaged_resources_are_never_deleted():
    actual = {"old-api": res("service"), "console-bucket": res("bucket", managed=False)}
    assert ops(plan({}, actual)) == [("delete", "old-api")], "only delete what this tool owns"


def test_computed_attributes_are_not_drift():
    desired = {"db": want("database", size="large")}
    actual = {"db": res("database", size="large", id="db-123", arn="arn:x", status="available")}
    assert plan(desired, actual) == [], "ids and statuses are assigned by the cloud"


def test_list_order_is_not_drift():
    desired = {"web": want("service", subnets=["b", "a", "c"], tags={"x": ["2", "1"]})}
    actual = {"web": res("service", subnets=["c", "b", "a"], tags={"x": ["1", "2"]})}
    assert plan(desired, actual) == []


def test_in_place_change_is_an_update_with_both_values():
    desired = {"db": want("database", size="large")}
    actual = {"db": res("database", size="small")}
    actions = plan(desired, actual)
    assert ops(actions) == [("update", "db")]
    assert actions[0]["changes"] == {"size": ("small", "large")}


def test_changing_an_immutable_property_requires_replacement():
    desired = {"db": want("database", size="large", region="eu-west")}
    actual = {"db": res("database", size="large", region="us-east")}
    assert ops(plan(desired, actual)) == [("replace", "db")]


def test_changing_type_replaces_and_removed_property_is_drift():
    actions = plan({"q": want("fifo-queue")}, {"q": res("queue")})
    assert ops(actions) == [("replace", "q")]
    actions = plan({"q": want("queue")}, {"q": res("queue", retention=7)})
    assert actions[0]["changes"] == {"retention": (7, None)}


def test_plan_order_and_summary():
    desired = {"b": want("svc", n=2), "a": want("svc"), "z": want("svc", region="x")}
    actual = {"b": res("svc", n=1), "z": res("svc", region="y"), "gone": res("svc")}
    actions = plan(desired, actual)
    assert ops(actions) == [("create", "a"), ("update", "b"), ("replace", "z"), ("delete", "gone")]
    assert summary(actions) == "Plan: 1 to add, 1 to change, 1 to replace, 1 to destroy."
    assert "n: 1 -> 2" in describe(actions[1])
