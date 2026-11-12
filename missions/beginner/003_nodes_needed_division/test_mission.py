import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import nodes_needed, monthly_cost, spare_slots


def test_exact_fit_needs_no_extra_node():
    assert nodes_needed(8, 4) == 2


def test_leftover_pods_need_an_extra_node():
    assert nodes_needed(10, 4) == 3, "10 pods at 4 per node need 3 whole nodes"


def test_single_pod_needs_one_node():
    assert nodes_needed(1, 110) == 1


def test_zero_pods_need_zero_nodes():
    assert nodes_needed(0, 4) == 0


def test_node_count_is_an_int():
    assert isinstance(nodes_needed(10, 4), int), "you cannot order 2.5 servers"


def test_monthly_cost_uses_whole_nodes():
    assert monthly_cost(10, 4, 70) == 210


def test_spare_slots():
    assert spare_slots(10, 4) == 2
