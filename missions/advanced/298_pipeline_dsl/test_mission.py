import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import ParseError, max_parallelism, parse, render, run_order, tokenize


def error_for(text):
    try:
        parse(text)
    except ParseError as exc:
        return exc
    raise AssertionError(f"{text!r} should not parse")


def test_stages_and_parallel_jobs():
    assert parse("build -> test & lint -> deploy") == [["build"], ["test", "lint"], ["deploy"]]
    assert parse("only") == [["only"]]


def test_hyphenated_job_names_are_allowed():
    assert parse("unit-test & lint-py -> push-image") == [["unit-test", "lint-py"], ["push-image"]]


def test_whitespace_is_optional_and_arrows_survive_hyphens():
    assert parse("build->test&lint->deploy") == [["build"], ["test", "lint"], ["deploy"]]
    assert [t[0] for t in tokenize("a->b")] == ["name", "arrow", "name"]


def test_trailing_arrow_is_an_error():
    exc = error_for("build -> test ->")
    assert exc.message == "expected a job name"
    assert exc.pos == len("build -> test ->")


def test_duplicate_job_names_are_rejected_with_their_position():
    exc = error_for("build -> test & build")
    assert "duplicate job 'build'" in exc.message
    assert exc.pos == 16


def test_error_position_points_at_the_offending_token():
    assert error_for("build -> & test").pos == 9
    assert error_for("build -> te$t").pos == 11
    assert error_for("build test").pos == 6


def test_empty_input_and_helpers():
    assert error_for("   ").pos == 3
    stages = parse("a -> b & c & d")
    assert render(stages) == "a -> b & c & d"
    assert run_order(stages)[1] == (1, "b")
    assert max_parallelism(stages) == 3
