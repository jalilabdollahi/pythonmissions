import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken

COMBINED = (
    '203.0.113.5 - alice [12/Mar/2025:10:00:01 +0000] "GET /api/items?page=2 HTTP/1.1" '
    '200 512 "https://shop.example/" "Mozilla/5.0 (X11)"'
)
COMMON = '198.51.100.7 - - [12/Mar/2025:10:00:02 +0000] "POST /login HTTP/1.1" 302 0'
FORWARDED = COMBINED + ' "10.1.2.3"'


def test_combined_line_fields():
    r = broken.parse_line(COMBINED)
    assert r["ip"] == "203.0.113.5"
    assert r["user"] == "alice"
    assert r["method"] == "GET" and r["path"] == "/api/items?page=2"
    assert r["status"] == 200 and r["bytes"] == 512
    assert r["referer"] == "https://shop.example/"
    assert r["agent"] == "Mozilla/5.0 (X11)"


def test_common_format_without_referer_and_agent_still_parses():
    r = broken.parse_line(COMMON)
    assert r is not None, "common-format lines have no referer/agent; that tail must be optional"
    assert r["status"] == 302
    assert r["referer"] is None and r["agent"] is None


def test_agent_stops_at_its_own_closing_quote():
    r = broken.parse_line(FORWARDED)
    assert r["agent"] == "Mozilla/5.0 (X11)", "a greedy .* in the agent group swallows the xff field"
    assert r["xff"] == "10.1.2.3"


def test_dash_bytes_become_zero():
    line = '10.0.0.9 - - [12/Mar/2025:10:00:03 +0000] "HEAD /health HTTP/1.1" 304 -'
    r = broken.parse_line(line)
    assert r is not None and r["bytes"] == 0


def test_garbage_line_returns_none():
    assert broken.parse_line("this is not a log line") is None


def test_parse_lines_counts_bad_and_totals_bytes():
    lines = [COMBINED, "", "garbage", COMMON, FORWARDED]
    records, bad = broken.parse_lines(lines)
    assert bad == 1
    assert len(records) == 3
    assert broken.total_bytes(records) == 512 + 0 + 512
