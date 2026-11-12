import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_overrides_are_visible_inside_the_block():
    env = {"REGION": "eu-west"}
    with broken.temporary_env(env, REGION="us-east", DEBUG="1"):
        assert broken.describe(env) == "region=us-east debug=1"


def test_existing_values_are_restored():
    env = {"REGION": "eu-west"}
    with broken.temporary_env(env, REGION="us-east"):
        pass
    assert env == {"REGION": "eu-west"}


def test_new_variables_are_removed_again():
    env = {}
    with broken.temporary_env(env, DEBUG="1"):
        pass
    assert env == {}, "a variable that did not exist before must not exist afterwards"


def test_environment_is_restored_when_block_raises():
    env = {"REGION": "eu-west"}
    with pytest.raises(RuntimeError):
        with broken.temporary_env(env, REGION="ap-south", DEBUG="1"):
            raise RuntimeError("scenario failed")
    assert env == {"REGION": "eu-west"}, "restore must run in a finally block"


def test_yields_the_mapping():
    env = {}
    with broken.temporary_env(env, A="1") as seen:
        assert seen is env


def test_working_directory_changes_and_returns(tmp_path):
    start = os.getcwd()
    target = tmp_path / "work"
    target.mkdir()
    try:
        with broken.working_directory(target) as inside:
            assert os.path.samefile(inside, target)
        assert os.path.samefile(os.getcwd(), start), "must return to the original directory"
    finally:
        os.chdir(start)


def test_working_directory_returns_even_on_error(tmp_path):
    start = os.getcwd()
    try:
        with pytest.raises(KeyError):
            with broken.working_directory(tmp_path):
                raise KeyError("x")
        assert os.path.samefile(os.getcwd(), start)
    finally:
        os.chdir(start)
