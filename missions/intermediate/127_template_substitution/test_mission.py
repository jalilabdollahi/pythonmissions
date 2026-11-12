import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

UNIT = "ExecStart=/opt/app --port $port --region ${region}\nPrice=$$5\n"


def test_find_placeholders_both_syntaxes():
    assert broken.find_placeholders(UNIT) == ["port", "region"]


def test_braced_only_placeholder_is_found():
    assert broken.find_placeholders("name=${svc}") == ["svc"], "${name} uses the 'braced' group"


def test_escaped_dollar_is_not_a_placeholder():
    assert broken.find_placeholders("cost $$5") == []


def test_render_all_values_present():
    out, missing = broken.render(UNIT, {"port": 8080, "region": "eu"})
    assert out == "ExecStart=/opt/app --port 8080 --region eu\nPrice=$5\n"
    assert missing == []


def test_missing_key_does_not_raise_and_is_reported():
    out, missing = broken.render(UNIT, {"port": 80})
    assert missing == ["region"]
    assert "--port 80" in out
    assert "${region}" in out, "unknown placeholders are left in place"


def test_zero_and_empty_string_count_as_provided():
    out, missing = broken.render("a=$a b=$b", {"a": 0, "b": ""})
    assert missing == []
    assert out == "a=0 b="


def test_render_all_reports_union_of_missing():
    outputs, missing = broken.render_all({"x": "$a $b", "y": "$b $c"}, {"b": 1})
    assert missing == ["a", "c"]
    assert outputs["x"] == "$a 1"
