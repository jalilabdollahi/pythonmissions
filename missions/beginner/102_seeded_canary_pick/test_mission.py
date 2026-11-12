import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import random

import pytest

from broken import pick_canaries, plan_waves

FLEET = [f"freight-{n:02d}" for n in range(1, 13)]


def test_same_seed_gives_same_canaries():
    assert pick_canaries(FLEET, 3, 7) == pick_canaries(FLEET, 3, 7), "a logged seed must replay the same draw"


def test_global_random_state_does_not_leak_in():
    random.seed(1)
    first = pick_canaries(FLEET, 3, 99)
    random.seed(2)
    second = pick_canaries(FLEET, 3, 99)
    assert first == second, "use a private random.Random(seed), not the shared global generator"


def test_input_order_does_not_matter():
    assert pick_canaries(FLEET, 4, 5) == pick_canaries(list(reversed(FLEET)), 4, 5)


def test_different_seeds_can_choose_different_hosts():
    draws = {tuple(pick_canaries(FLEET, 3, s)) for s in range(10)}
    assert len(draws) > 1


def test_canaries_are_distinct_members_of_the_fleet():
    picked = pick_canaries(FLEET, 5, 3)
    assert len(set(picked)) == 5 and set(picked) <= set(FLEET)


def test_too_many_canaries_raises():
    with pytest.raises(ValueError):
        pick_canaries(FLEET, 50, 1)


def test_waves_cover_every_host_once_and_replay():
    waves = plan_waves(FLEET, 5, 11)
    flat = [h for w in waves for h in w]
    assert sorted(flat) == sorted(FLEET)
    assert waves == plan_waves(FLEET, 5, 11)
