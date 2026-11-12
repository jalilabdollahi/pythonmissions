import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import FaultInjector, InjectedFault, Rule, drill


def make(seed=7, **rules):
    sleeps = []
    return FaultInjector(seed, rules, sleeps.append), sleeps


def ok():
    return "ok"


def test_same_seed_gives_the_same_failures():
    a, _ = make(payments=Rule(0.5))
    b, _ = make(payments=Rule(0.5))
    random.random()  # unrelated code touching the global generator must not matter
    assert drill(a, "payments", ok, 40) == drill(b, "payments", ok, 40)


def test_different_seeds_give_different_failures():
    a, _ = make(seed=1, payments=Rule(0.5))
    b, _ = make(seed=2, payments=Rule(0.5))
    assert drill(a, "payments", ok, 40) != drill(b, "payments", ok, 40)


def test_targets_have_independent_streams():
    both, _ = make(payments=Rule(0.5), search=Rule(0.5))
    pay = drill(both, "payments", ok, 40)
    search = drill(both, "search", ok, 40)
    assert pay != search, "two targets with the same rate must not fail in lockstep"


def test_other_targets_do_not_disturb_a_targets_sequence():
    alone, _ = make(payments=Rule(0.5))
    busy, _ = make(payments=Rule(0.5), search=Rule(0.5))
    expected = drill(alone, "payments", ok, 30)
    got = []
    for _ in range(30):
        drill(busy, "search", ok, 3)
        got.append(drill(busy, "payments", ok, 1))
    assert "".join(got) == expected


def test_latency_is_converted_to_seconds_and_applied_before_the_roll():
    inj, sleeps = make(search=Rule(error_rate=1.0, latency_ms=250))
    try:
        inj.call("search", ok)
    except InjectedFault:
        pass
    assert sleeps == [0.25]


def test_injected_failure_never_runs_the_real_call():
    inj, _ = make(payments=Rule(1.0))
    charged = []
    try:
        inj.call("payments", lambda: charged.append("card charged"))
    except InjectedFault:
        pass
    assert charged == [], "a chaos failure must happen instead of the call, not after it"
    assert inj.injected["payments"] == 1


def test_unruled_targets_pass_through_and_rates_are_validated():
    inj, sleeps = make(payments=Rule(1.0))
    assert inj.call("inventory", ok) == "ok"
    assert inj.wrap("inventory", lambda x: x * 2)(21) == 42
    assert sleeps == []
    try:
        Rule(1.5)
    except ValueError:
        return
    raise AssertionError("error_rate above 1 must raise ValueError")


def test_rules_from_spec():
    from broken import rules_from_spec

    rules = rules_from_spec({"payments": {"error_rate": 0.2, "latency_ms": 50}})
    assert rules["payments"].error_rate == 0.2 and rules["payments"].latency_ms == 50
