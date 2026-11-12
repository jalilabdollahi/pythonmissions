import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

WHEN = datetime(2024, 5, 1, 12, 0, tzinfo=timezone.utc)


def make(**kwargs):
    return broken.build_alert("disk full", "db1 is at 98%", ["oncall@x.example", "lead@x.example"], date=WHEN, **kwargs)


def test_multiple_recipients_share_one_header():
    msg = make()
    assert msg["To"] == "oncall@x.example, lead@x.example"
    assert msg["From"] == "alerts@harbor.example"
    assert msg["Date"] == "Wed, 01 May 2024 12:00:00 +0000"


def test_cc_header_and_body():
    msg = make(cc=["boss@x.example"])
    assert msg["Cc"] == "boss@x.example"
    assert msg.get_content().strip() == "db1 is at 98%"


def test_urgent_marking_keeps_a_single_subject():
    msg = broken.mark_urgent(make())
    assert msg.get_all("Subject") == ["[URGENT] disk full"]
    assert msg["X-Priority"] == "1"


def test_envelope_contains_to_and_cc():
    msg = make(cc=["boss@x.example", "oncall@x.example"])
    assert broken.envelope_recipients(msg) == ["boss@x.example", "lead@x.example", "oncall@x.example"], "Cc people need the mail too"


def test_envelope_handles_display_names_with_commas():
    msg = broken.build_alert("s", "b", ['"Doe, Jane" <jane@x.example>'], cc=["Bob <bob@x.example>"])
    assert broken.envelope_recipients(msg) == ["bob@x.example", "jane@x.example"]


def test_html_alternative_is_added():
    msg = broken.add_html(make(), "<p>db1 is at <b>98%</b></p>")
    assert msg.get_content_type() == "multipart/alternative"
    html_part = msg.get_body(preferencelist=("html",))
    assert "<b>98%</b>" in html_part.get_content()


def test_describe_summary():
    msg = make(cc=["boss@x.example"])
    assert broken.describe(msg) == "disk full -> 3 recipient(s), parts: text/plain"
