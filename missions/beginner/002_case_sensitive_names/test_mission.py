import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import deploy_summary, summarize_all


def test_summary_mentions_host():
    assert "pay-api-1" in deploy_summary("pay-api-1", "v2.14.0", "prod")


def test_summary_exact_format():
    assert deploy_summary("pay-api-1", "v2.14.0", "prod") == "v2.14.0 deployed to pay-api-1 (PROD)"


def test_environment_is_uppercased():
    assert deploy_summary("w1", "v1", "staging").endswith("(STAGING)")


def test_summarize_all_one_line_per_host():
    lines = summarize_all(["a", "b", "c"], "v3", "qa")
    assert len(lines) == 3
    assert lines[2] == "v3 deployed to c (QA)"


def test_summarize_all_empty():
    assert summarize_all([], "v3", "qa") == []
