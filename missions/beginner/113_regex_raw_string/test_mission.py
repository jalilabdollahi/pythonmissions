import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import find_hosts, find_ports, summarize, mentions_default_port

NOTE = "failover from db-12 to db-7; mydb-3 untouched, db-9x typo; replicas on port=5432 and port=6432, support=1"


def test_hosts_are_found_in_order():
    assert find_hosts(NOTE) == ["db-12", "db-7"], "write regex patterns as raw strings: r\"\\b...\""


def test_partial_names_are_ignored():
    assert "mydb-3" not in find_hosts(NOTE)
    assert "db-9" not in find_hosts(NOTE)


def test_ports_are_ints():
    assert find_ports(NOTE) == [5432, 6432]


def test_port_must_start_at_word_boundary():
    assert find_ports("support=80 and port=22") == [22]


def test_empty_text_has_no_matches():
    assert find_hosts("nothing here") == []
    assert find_ports("") == []


def test_summarize_and_default_port():
    assert summarize(NOTE) == "2 hosts, 2 ports"
    assert mentions_default_port(NOTE) is True
