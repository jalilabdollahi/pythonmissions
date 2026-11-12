import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_each_check_probes_its_own_host():
    seen = []
    checks = broken.build_checks(["web-1", "web-2", "db-1"], lambda host: seen.append(host) or host)
    for check in checks.values():
        check()
    assert seen == ["web-1", "web-2", "db-1"], "all lambdas share the loop variable unless it is bound"


def test_run_all_returns_one_result_per_host():
    checks = broken.build_checks(["a", "b"], lambda host: host.upper())
    assert broken.run_all(checks) == {"a": "A", "b": "B"}


def test_rules_use_their_own_limit():
    rules = broken.build_threshold_rules({"cpu": 80, "mem": 90, "disk": 95})
    assert rules["cpu"](85) is True
    assert rules["mem"](85) is False
    assert rules["disk"](94) is False


def test_failing_rules_with_readings():
    rules = broken.build_threshold_rules({"cpu": 80, "mem": 90})
    assert broken.failing_rules(rules, {"cpu": 81, "mem": 50}) == ["cpu"]


def test_summary_text():
    checks = broken.build_checks(["a", "b", "c"], lambda host: host != "b")
    assert broken.summarize(broken.run_all(checks)) == "2/3 checks passed"


def test_counter_counts_up():
    tick = broken.make_counter()
    assert [tick(), tick(), tick()] == [1, 2, 3]


def test_counters_are_independent():
    first, second = broken.make_counter(), broken.make_counter()
    first()
    first()
    assert second() == 1
