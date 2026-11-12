import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import build_blocklist, unique_offenders

LOG = [
    "203.0.113.50 - GET /wp-login.php",
    "198.51.100.7 - GET /",
    "203.0.113.50 - GET /xmlrpc.php",
    "192.0.2.200 - POST /login",
    "",
    "198.51.100.7 - GET /about",
    "10.9.8.7 - GET /admin",
    "192.0.2.14 - GET /robots.txt",
    "172.16.0.3 - GET /status",
    "10.9.8.7 - GET /admin/users",
]
ORDER = ["203.0.113.50", "198.51.100.7", "192.0.2.200", "10.9.8.7", "192.0.2.14", "172.16.0.3"]


def test_duplicates_are_removed():
    result = unique_offenders(LOG)
    assert len(result) == len(set(result)) == 6, "each IP must appear exactly once"


def test_first_seen_order_is_preserved():
    assert unique_offenders(LOG) == ORDER, "IPs must stay in the order they first appeared"


def test_blank_lines_are_ignored():
    assert unique_offenders(["", "  ", "10.0.0.1 - hi"]) == ["10.0.0.1"]


def test_blocklist_keeps_worst_offenders_when_capped():
    assert build_blocklist(LOG, 3) == ORDER[:3], "the cap must keep the earliest offenders"


def test_empty_log_gives_empty_blocklist():
    assert build_blocklist([], 10) == []
