import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import coverage_report, stale_monitors, unmonitored_hosts

CMDB = ["db-01", "db-02", "web-01", "web-02", "cache-01"]
MONITORED = ["web-01", "web-02", "cache-01", "old-ftp-01"]


def test_hosts_without_monitoring_are_listed():
    assert unmonitored_hosts(CMDB, MONITORED) == ["db-01", "db-02"], "db hosts have no monitor and must be reported"


def test_monitored_hosts_are_not_reported_missing():
    assert "web-01" not in unmonitored_hosts(CMDB, MONITORED)


def test_stale_monitor_for_decommissioned_host():
    assert stale_monitors(CMDB, MONITORED) == ["old-ftp-01"], "only monitors with no inventory host are stale"


def test_stale_report_excludes_unmonitored_hosts():
    assert "db-01" not in stale_monitors(CMDB, MONITORED), "an unmonitored host is not a stale monitor"


def test_full_coverage_gives_empty_gaps():
    assert unmonitored_hosts(["a", "b"], ["a", "b"]) == []


def test_coverage_report_counts():
    report = coverage_report(CMDB, MONITORED)
    assert report == {"covered": 3, "missing": ["db-01", "db-02"], "stale": ["old-ftp-01"]}
