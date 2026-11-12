import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import count_exposed, scan_matrix

OPEN = {("web", 80), ("web", 443), ("db", 5432), ("jump", 22), ("jump", 80)}


def probe(host, port):
    return (host, port) in OPEN


HOSTS = ["web", "db", "jump"]
PORTS = [22, 80, 443, 5432]


def test_every_host_appears_in_result():
    assert set(scan_matrix(HOSTS, PORTS, probe)) == set(HOSTS), "results must be stored for each host, not just the last"


def test_each_host_gets_only_its_own_ports():
    result = scan_matrix(HOSTS, PORTS, probe)
    assert result["web"] == [80, 443]
    assert result["db"] == [5432], "db must not inherit web's ports"
    assert result["jump"] == [22, 80]


def test_host_with_nothing_open_gets_empty_list():
    assert scan_matrix(["ghost"], PORTS, probe) == {"ghost": []}


def test_empty_host_list():
    assert scan_matrix([], PORTS, probe) == {}


def test_count_exposed_adds_up_all_hosts():
    assert count_exposed(scan_matrix(HOSTS, PORTS, probe)) == 5
