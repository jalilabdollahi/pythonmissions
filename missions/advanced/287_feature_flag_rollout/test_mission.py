import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken
from broken import Flag, FlagStore, bucket, cohort, exposure, is_enabled, next_step, ramp_is_safe

USERS = [f"user-{i}" for i in range(400)]


def test_bucket_matches_stable_reference_values():
    assert bucket("checkout-v2", "user-42") == 2945
    assert bucket("checkout-v2", "user-7") == 8440, "must not depend on the per-process hash seed"


def test_same_user_always_gets_the_same_answer():
    flag = Flag("checkout-v2", percent=50)
    first = [is_enabled(flag, u) for u in USERS]
    assert first == [is_enabled(flag, u) for u in USERS]


def test_different_flags_pick_different_cohorts():
    a = cohort(Flag("new-search", percent=50), USERS)
    b = cohort(Flag("dark-mode", percent=50), USERS)
    assert a != b, "flags must be bucketed independently"


def test_raising_the_percentage_only_adds_users():
    flag = Flag("checkout-v2", percent=10)
    assert ramp_is_safe(flag, USERS, 20)
    assert cohort(flag, USERS) <= cohort(Flag("checkout-v2", percent=60), USERS)
    assert 0.03 < exposure(Flag("checkout-v2", percent=10), USERS) < 0.18


def test_zero_and_hundred_percent_are_exact():
    assert cohort(Flag("f", percent=0), USERS) == set()
    assert cohort(Flag("f", percent=100), USERS) == set(USERS)


def test_percent_threshold_rounds_instead_of_truncating(monkeypatch):
    monkeypatch.setattr(broken, "bucket", lambda flag, user: 819)
    flag = Flag("f", percent=8.2)  # 8.2 * 100 is 819.9999999999999 in floating point
    assert is_enabled(flag, "anyone"), "bucket 819 is below 8.20 percent"
    monkeypatch.setattr(broken, "bucket", lambda flag, user: 820)
    assert not is_enabled(flag, "anyone")


def test_deny_beats_allow_and_kill_switch_beats_both():
    flag = Flag("f", percent=0, allow={"qa"}, deny={"banned"})
    assert is_enabled(flag, "qa")
    assert not is_enabled(Flag("f", percent=100, deny={"banned"}), "banned")
    killed = Flag("f", percent=100, enabled=False, allow={"qa"})
    assert not is_enabled(killed, "qa"), "the kill switch must disable everyone, even the allow list"


def test_ramp_schedule_and_unknown_flags():
    assert next_step(5, [1, 5, 25, 100]) == 25
    assert next_step(100, [1, 5, 25, 100]) is None
    store = FlagStore([Flag("checkout-v2", percent=1)])
    assert store.advance("checkout-v2", [1, 5, 25]) == 5
    assert store.check("checkuot-v2", "user-1") is False, "a misspelled flag is off"
