import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_service_unit_name():
    assert broken.service_name("nginx.service") == "nginx"


def test_timer_unit_name_is_not_truncated():
    assert broken.service_name("backup.timer") == "backup", "suffix lengths differ between unit types"


def test_dotted_names_keep_inner_dots():
    assert broken.service_name("my.app.service") == "my.app"


def test_socket_name():
    assert broken.service_name("docker.socket") == "docker"


def test_inventory_pairs_are_sorted():
    got = broken.inventory(["b.timer", "a.service", "c.socket"])
    assert got == [("a", "service"), ("b", "timer"), ("c", "socket")]


def test_timers_only():
    assert broken.timers_only(["x.service", "cleanup.timer"]) == ["cleanup"]
