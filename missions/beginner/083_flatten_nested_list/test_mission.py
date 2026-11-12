import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import all_ips, ip_count, ips_for_firewall, cidrs_with_ips, busiest_subnet

PLAN = [
    {"cidr": "10.0.1.0/24", "ips": ["10.0.1.5", "10.0.1.9"]},
    {"cidr": "10.0.2.0/24", "ips": []},
    {"cidr": "10.0.3.0/24", "ips": ["10.0.3.4"]},
]


def test_all_ips_is_flat_and_ordered():
    assert all_ips(PLAN) == ["10.0.1.5", "10.0.1.9", "10.0.3.4"], "outer loop first, inner loop second"


def test_all_ips_of_empty_input():
    assert all_ips([]) == []
    assert all_ips([{"cidr": "x", "ips": []}]) == []


def test_ip_count():
    assert ip_count(PLAN) == 3


def test_firewall_rules():
    assert ips_for_firewall(PLAN)[0] == "allow 10.0.1.5"
    assert len(ips_for_firewall(PLAN)) == 3


def test_cidrs_with_ips_skips_empty_subnets():
    assert cidrs_with_ips(PLAN) == ["10.0.1.0/24", "10.0.3.0/24"]


def test_busiest_subnet():
    assert busiest_subnet(PLAN) == "10.0.1.0/24"
    assert busiest_subnet([]) is None
