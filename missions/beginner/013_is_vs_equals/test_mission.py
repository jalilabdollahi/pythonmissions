import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import needs_approval, deploy_gate


def runtime_text(*pieces):
    # builds a new string object, like text that came from argv or a file
    return "".join(pieces)


def test_prod_built_at_runtime_needs_approval():
    assert needs_approval(runtime_text("pr", "od")) is True, "equal text must match even if it is a different object"


def test_uppercase_prod_needs_approval():
    assert needs_approval(runtime_text("PR", "OD")) is True


def test_spaces_are_ignored():
    assert needs_approval(runtime_text("  pr", "od ")) is True


def test_staging_does_not_need_approval():
    assert needs_approval(runtime_text("stag", "ing")) is False


def test_gate_messages():
    assert deploy_gate(runtime_text("pr", "od")) == "manual approval required"
    assert deploy_gate(runtime_text("q", "a")) == "auto deploy"
