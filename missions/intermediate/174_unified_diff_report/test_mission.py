import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


OLD = "listen 80;\nworkers 2;\nlog off;"
NEW = "listen 443;\nworkers 2;\nlog off;\ngzip on;"


def test_diff_has_expected_rows_and_no_blank_lines():
    out = broken.unified(OLD, NEW, "lb")
    assert out.splitlines() == [
        "--- lb.deployed",
        "+++ lb.desired",
        "@@ -1,3 +1,4 @@",
        "-listen 80;",
        "+listen 443;",
        " workers 2;",
        " log off;",
        "+gzip on;",
    ], "header rows and body rows must be joined with a single newline"


def test_diff_direction_is_deployed_to_desired():
    out = broken.unified("a", "b", "x")
    assert "-a" in out.splitlines() and "+b" in out.splitlines()


def test_labels_use_the_file_name():
    out = broken.unified("a", "b", "haproxy.cfg")
    assert "--- haproxy.cfg.deployed" in out and "+++ haproxy.cfg.desired" in out


def test_count_changes_ignores_file_headers():
    out = broken.unified(OLD, NEW, "lb")
    assert broken.count_changes(out) == (2, 1)


def test_count_changes_of_empty_diff():
    assert broken.count_changes("") == (0, 0)


def test_identical_files_have_empty_diff():
    assert broken.unified(OLD, OLD, "lb") == ""


def test_drift_report_lists_only_drifting_files_sorted():
    files = {"z.cfg": ("a", "b"), "ok.cfg": ("same", "same"), "a.cfg": ("1", "2")}
    report = broken.drift_report(files)
    assert report.index("a.cfg") < report.index("z.cfg")
    assert "ok.cfg" not in report
    assert "\n\n--- z.cfg.deployed" in report


def test_drift_report_when_clean():
    assert broken.drift_report({"a": ("x", "x")}) == "no drift"
