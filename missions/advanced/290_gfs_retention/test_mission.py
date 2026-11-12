import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import names_to_delete, parse_backup_name, plan, is_stale, savings, select_keep, tiers_for


def at(y, m, d, h=2):
    return datetime(y, m, d, h)


def test_daily_counts_days_not_files():
    backups = [at(2024, 6, 10, 2), at(2024, 6, 10, 14), at(2024, 6, 10, 23), at(2024, 6, 9, 2)]
    keep = select_keep(backups, daily=2, weekly=0, monthly=0)
    assert keep == {at(2024, 6, 10, 23), at(2024, 6, 9, 2)}, "newest of each of the last 2 days"


def test_weekly_keeps_the_newest_backup_of_each_week():
    backups = [at(2024, 6, 3), at(2024, 6, 5), at(2024, 6, 7), at(2024, 6, 12), at(2024, 6, 14)]
    keep = select_keep(backups, daily=0, weekly=2, monthly=0)
    assert keep == {at(2024, 6, 14), at(2024, 6, 7)}


def test_monthly_keeps_the_newest_backup_of_each_month():
    backups = [at(2024, 4, 1), at(2024, 4, 29), at(2024, 5, 2), at(2024, 5, 30)]
    keep = select_keep(backups, daily=0, weekly=0, monthly=2)
    assert keep == {at(2024, 4, 29), at(2024, 5, 30)}


def test_same_week_number_in_different_years_is_not_the_same_week():
    old, new = at(2023, 6, 14), at(2024, 6, 12)
    keep = select_keep([old, new], daily=0, weekly=4, monthly=0)
    assert keep == {old, new}, "ISO week 24 of 2023 and of 2024 are different weeks"


def test_same_month_in_different_years_is_not_the_same_month():
    old, new = at(2023, 3, 4), at(2024, 3, 5)
    keep = select_keep([old, new], daily=0, weekly=0, monthly=6)
    assert keep == {old, new}, "March 2023 must survive next to March 2024"


def test_union_of_all_three_tiers():
    backups = [at(2024, 6, d) for d in range(1, 29)]
    keep = select_keep(backups, daily=3, weekly=2, monthly=1)
    assert at(2024, 6, 28) in keep and at(2024, 6, 27) in keep and at(2024, 6, 26) in keep
    assert at(2024, 6, 23) in keep, "Sunday 23rd is the newest backup of the previous week"
    assert len(keep) == 4


def test_plan_and_file_names():
    names = ["db-20240601T0200.tar.gz", "db-20240602T0200.tar.gz", "db-20240602T1400.tar.gz"]
    assert parse_backup_name(names[2]) == at(2024, 6, 2, 14)
    assert names_to_delete(names, daily=1, weekly=0, monthly=0) == names[:2]
    both = plan([at(2024, 6, 1), at(2024, 6, 2)], daily=1, weekly=0, monthly=0)
    assert both == {"keep": [at(2024, 6, 2)], "delete": [at(2024, 6, 1)]}


def test_tiers_explain_why_each_backup_is_kept():
    backups = [at(2024, 6, 10), at(2024, 6, 9), at(2024, 5, 31)]
    tiers = tiers_for(backups, daily=1, weekly=1, monthly=2)
    assert tiers["son"] == [at(2024, 6, 10)]
    assert tiers["father"] == [at(2024, 6, 10)]
    assert tiers["grandfather"] == [at(2024, 5, 31), at(2024, 6, 10)]


def test_staleness_and_savings():
    assert not is_stale([at(2024, 6, 10)], at(2024, 6, 11, 1))
    assert is_stale([at(2024, 6, 10)], at(2024, 6, 12))
    assert is_stale([], at(2024, 6, 12))
    backups = [at(2024, 6, d) for d in range(1, 11)]
    assert savings(backups, daily=2, weekly=0, monthly=0) == 0.8
