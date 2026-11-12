import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import Inventory


def test_add_and_get_roundtrip(tmp_path):
    inv = Inventory(tmp_path / "inv.db")
    inv.add_host("web-01", "r1", 16)
    assert inv.get_host("web-01") == ("web-01", "r1", 16)


def test_unknown_host_is_none(tmp_path):
    inv = Inventory(tmp_path / "inv.db")
    assert inv.get_host("ghost") is None


def test_hostnames_with_apostrophes_are_stored_verbatim(tmp_path):
    inv = Inventory(tmp_path / "inv.db")
    inv.add_host("o'brien-lab", "r'2", 4)
    assert inv.get_host("o'brien-lab") == ("o'brien-lab", "r'2", 4)


def test_injection_attempt_is_just_a_name(tmp_path):
    inv = Inventory(tmp_path / "inv.db")
    inv.add_host("web-01", "r1", 8)
    inv.add_host("x', 'r9', 1); DROP TABLE hosts; --", "r1", 2)
    assert inv.get_host("web-01") is not None
    assert inv.cpu_by_rack() == {"r1": 10}


def test_move_returns_rowcount_and_updates(tmp_path):
    inv = Inventory(tmp_path / "inv.db")
    inv.add_host("web-01", "r1", 8)
    assert inv.move_to_rack("web-01", "r5") == 1
    assert inv.move_to_rack("ghost", "r5") == 0
    assert inv.get_host("web-01")[1] == "r5"


def test_moves_are_committed_for_other_connections(tmp_path):
    path = tmp_path / "inv.db"
    first = Inventory(path)
    first.add_host("web-01", "r1", 8)
    first.move_to_rack("web-01", "r5")
    second = Inventory(path)
    assert second.get_host("web-01")[1] == "r5", "UPDATE needs a commit to become visible"


def test_cpu_totals_and_rack_listing(tmp_path):
    inv = Inventory(tmp_path / "inv.db")
    inv.add_host("b", "r1", 8)
    inv.add_host("a", "r1", 16)
    inv.add_host("c", "r2", 4)
    assert inv.cpu_by_rack() == {"r1": 24, "r2": 4}
    assert inv.hosts_in_rack("r1") == ["a", "b"]
