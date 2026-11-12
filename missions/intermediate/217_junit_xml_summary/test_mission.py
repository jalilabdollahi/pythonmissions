import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

SUITE = """
<testsuite name="api" tests="5">
  <testcase classname="api.auth" name="test_login" time="0.5"/>
  <testcase classname="api.auth" name="test_logout" time="0.25">
    <failure message="expected 204">AssertionError</failure>
  </testcase>
  <testcase classname="api.db" name="test_pool" time="1.0">
    <error message="ConnectionRefused">Traceback</error>
  </testcase>
  <testcase classname="api.db" name="test_slow" time="0">
    <skipped message="needs gpu"/>
  </testcase>
  <testcase classname="api.db" name="test_query" time="0.125"/>
</testsuite>
"""

WRAPPED = """
<testsuites>
  <testsuite name="a"><testcase classname="a" name="t1"/><testcase classname="a" name="t2"/></testsuite>
  <testsuite name="b"><testcase classname="b" name="t3"><failure/></testcase></testsuite>
</testsuites>
"""


def test_counts_of_each_outcome():
    result = broken.summarize(SUITE)
    assert (result["passed"], result["failed"], result["errors"], result["skipped"]) == (2, 1, 1, 1)


def test_errors_are_not_failures():
    result = broken.summarize(SUITE)
    assert result["failed"] == 1, "a crashed test is an error, not a failed assertion"
    assert result["errors"] == 1


def test_skipped_tests_do_not_count_as_passed():
    result = broken.summarize(SUITE)
    assert result["passed"] == 2
    assert result["skipped"] == 1


def test_failing_names_include_failures_and_errors():
    assert broken.summarize(SUITE)["failures"] == ["api.auth.test_logout", "api.db.test_pool"]


def test_testsuites_wrapper_is_supported():
    result = broken.summarize(WRAPPED)
    assert (result["passed"], result["failed"]) == (2, 1)


def test_digest_line_and_green_flag():
    result = broken.summarize(SUITE)
    assert not broken.is_green(result)
    assert broken.digest(result) == "RED: 2/5 passed, 1 failed, 1 errors, 1 skipped"
    clean = broken.summarize("<testsuite><testcase classname='a' name='b'/></testsuite>")
    assert broken.is_green(clean)
    assert broken.digest(clean).startswith("GREEN: 1/1 passed")


def test_total_time_adds_up_durations():
    assert broken.total_time(SUITE) == 1.875
