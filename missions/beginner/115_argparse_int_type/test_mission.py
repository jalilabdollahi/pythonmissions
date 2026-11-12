import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import parse_args, rollout_steps, describe


def test_replicas_is_an_int_when_given():
    args = parse_args(["api", "--replicas", "7"])
    assert args.replicas == 7, "add type=int so argparse converts the text"


def test_batch_size_is_an_int_when_given():
    assert parse_args(["api", "--batch-size", "3"]).batch_size == 3


def test_defaults():
    args = parse_args(["api"])
    assert (args.replicas, args.batch_size) == (2, 1)


def test_non_numeric_value_is_a_usage_error():
    with pytest.raises(SystemExit):
        parse_args(["api", "--replicas", "many"])


def test_rollout_steps_rounds_up():
    assert rollout_steps(parse_args(["api", "--replicas", "7", "--batch-size", "3"])) == 3


def test_describe():
    assert describe(["api", "--replicas", "7", "--batch-size", "3"]) == "api: 7 replicas in 3 steps"
    assert describe(["web"]) == "web: 2 replicas in 2 steps"
