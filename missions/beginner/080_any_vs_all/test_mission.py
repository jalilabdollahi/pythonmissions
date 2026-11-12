import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import cluster_healthy, cluster_degraded, cluster_down, status, banner


def mk(*flags):
    return [{"name": f"c{i}", "up": f} for i, f in enumerate(flags)]


def test_all_nodes_up_is_healthy():
    assert cluster_healthy(mk(True, True, True))


def test_one_node_down_is_not_healthy():
    assert not cluster_healthy(mk(True, False, True)), "healthy means EVERY node is up"


def test_one_node_down_is_degraded():
    assert cluster_degraded(mk(True, False, True))


def test_all_up_is_not_degraded():
    assert not cluster_degraded(mk(True, True)), "degraded means AT LEAST ONE node is down"


def test_cluster_down_only_when_nothing_is_up():
    assert cluster_down(mk(False, False))
    assert not cluster_down(mk(False, True))
    assert cluster_down([])


def test_status_order():
    assert status(mk(False, False)) == "down"
    assert status(mk(True, False)) == "degraded"
    assert status(mk(True, True)) == "healthy"


def test_banner_names_the_dead_nodes():
    assert banner(mk(True, False, False)) == "DEGRADED: c1, c2"
    assert banner(mk(True)) == "HEALTHY"
