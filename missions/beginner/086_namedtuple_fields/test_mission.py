import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Backup, total_size_gb, failed_hosts, oldest, stale, summary

DATA = [
    Backup("db-mon", "db1", 100, 40, True),
    Backup("db-tue", "db1", 101, 42, False),
    Backup("web-old", "web1", 90, 5, True),
    Backup("web-bad", "web2", 99, 7, False),
]


def test_total_size_sums_gigabytes_not_days():
    assert total_size_gb(DATA) == 94, "read the size_gb field by name"


def test_total_size_of_nothing():
    assert total_size_gb([]) == 0


def test_failed_hosts_are_unique_and_sorted():
    assert failed_hosts(DATA) == ["db1", "web2"]


def test_failed_hosts_when_all_ok():
    assert failed_hosts([Backup("a", "h", 1, 1, True)]) == []


def test_oldest_uses_created_day():
    assert oldest(DATA) == "web-old"
    assert oldest([]) is None


def test_stale_means_more_than_seven_days_old():
    assert stale(DATA, 108) == ["db-mon", "web-bad", "web-old"]


def test_exactly_seven_days_old_is_not_stale():
    assert "db-tue" not in stale(DATA, 108)


def test_summary_line():
    assert summary(DATA, 108) == "4 backups, 94 GB, 3 stale"
