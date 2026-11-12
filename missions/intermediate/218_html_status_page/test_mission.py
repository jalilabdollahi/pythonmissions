import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_plain_service_row():
    row = broken.render_row({"name": "API", "status": "up", "detail": "all good"})
    assert row == '<tr class="up"><td>API</td><td title="all good">Operational</td></tr>'


def test_service_name_is_escaped_as_text():
    row = broken.render_row({"name": "<Billing & Invoices>", "status": "up"})
    assert "<td>&lt;Billing &amp; Invoices&gt;</td>" in row, "names are human input: escape them"
    assert "<Billing" not in row


def test_detail_quotes_cannot_break_the_attribute():
    row = broken.render_row({"name": "API", "status": "down", "detail": 'said "hi" & left'})
    assert 'title="said &quot;hi&quot; &amp; left"' in row


def test_script_injection_is_neutralised():
    row = broken.render_row({"name": "<script>alert(1)</script>", "status": "up", "detail": '"><script>'})
    assert "<script>" not in row


def test_unknown_status_is_shown_as_unknown():
    row = broken.render_row({"name": "X", "status": 'pwned"><b>'})
    assert row == '<tr class="unknown"><td>X</td><td title="">Unknown</td></tr>'


def test_down_beats_degraded_in_the_banner():
    services = [{"name": "a", "status": "degraded"}, {"name": "b", "status": "down"}]
    assert broken.overall(services) == "Major outage"


def test_other_banner_states():
    assert broken.overall([{"name": "a", "status": "degraded"}]) == "Partial outage"
    assert broken.overall([{"name": "a", "status": "up"}]) == "All systems operational"
    assert broken.overall([]) == "All systems operational"


def test_count_by_status():
    services = [{"name": "a", "status": "up"}, {"name": "b", "status": "up"}, {"name": "c", "status": "??"}]
    assert broken.count_by_status(services) == {"up": 2, "unknown": 1}


def test_page_escapes_title_and_contains_rows():
    page = broken.render_page("A&B Status", [{"name": "API", "status": "up"}])
    assert "<h1>A&amp;B Status</h1>" in page
    assert '<tr class="up">' in page
