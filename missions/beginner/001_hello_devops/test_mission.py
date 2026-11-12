import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import banner, replica_line, full_banner


def test_banner_includes_host_and_port():
    assert banner("lf-edge-07", 8080) == "Host lf-edge-07 is listening on port 8080"


def test_banner_with_other_port_number():
    assert banner("db-1", 5432) == "Host db-1 is listening on port 5432", "ints must be converted to text"


def test_replica_line_with_int_count():
    assert replica_line("router", 3) == "router is running 3 replicas"


def test_replica_line_with_zero_replicas():
    assert replica_line("batch", 0) == "batch is running 0 replicas"


def test_full_banner_has_two_lines():
    text = full_banner("lf-edge-07", 8080, "router", 3)
    assert text.split("\n") == ["Host lf-edge-07 is listening on port 8080", "router is running 3 replicas"]
