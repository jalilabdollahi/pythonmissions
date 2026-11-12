import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Machine, stand_up_lines

BOOT = 1_700_000_000
DAY = 86400


def test_uptime_seconds():
    assert Machine("a", BOOT).uptime_seconds(BOOT + 90) == 90


def test_uptime_days_uses_whole_days():
    m = Machine("a", BOOT)
    assert m.uptime_days(BOOT + 3 * DAY + 5000) == 3, "instance methods need self as first parameter"


def test_uptime_days_under_one_day_is_zero():
    assert Machine("a", BOOT).uptime_days(BOOT + 100) == 0


def test_needs_reboot_at_the_limit():
    m = Machine("a", BOOT)
    assert m.needs_reboot(BOOT + 30 * DAY, 30)
    assert not m.needs_reboot(BOOT + 29 * DAY, 30)


def test_label():
    assert Machine("gw-1", BOOT).label() == "gw-1 (booted 1700000000)"


def test_stand_up_lines():
    fleet = [Machine("gw-1", BOOT), Machine("gw-2", BOOT - 10 * DAY)]
    assert stand_up_lines(fleet, BOOT + DAY) == ["gw-1: 1d", "gw-2: 11d"]
