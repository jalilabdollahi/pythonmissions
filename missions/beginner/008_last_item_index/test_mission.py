import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import newest_backup, oldest_backup, restore_plan

BACKUPS = ["db-01.tar", "db-02.tar", "db-03.tar"]


def test_newest_is_last_item():
    assert newest_backup(BACKUPS) == "db-03.tar"


def test_newest_of_single_item():
    assert newest_backup(["only.tar"]) == "only.tar"


def test_newest_of_empty_list_is_none():
    assert newest_backup([]) is None, "an empty list has no newest backup"


def test_oldest_is_first_item():
    assert oldest_backup(BACKUPS) == "db-01.tar"


def test_restore_plan_message():
    assert restore_plan(BACKUPS) == "restore from db-03.tar"


def test_restore_plan_without_backups():
    assert restore_plan([]) == "no backups available"
