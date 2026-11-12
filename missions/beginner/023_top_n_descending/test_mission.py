import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import top_cpu, cpu_report

USAGE = {"nginx": 4.0, "batch-export": 97.5, "cron": 0.2, "etl": 55.1, "sshd": 0.1, "metrics": 12.0}


def test_busiest_process_comes_first():
    assert top_cpu(USAGE)[0] == "batch-export"


def test_top_three_in_descending_order():
    assert top_cpu(USAGE) == ["batch-export", "etl", "metrics"], "the three highest consumers, highest first"


def test_custom_n():
    assert top_cpu(USAGE, 1) == ["batch-export"]
    assert len(top_cpu(USAGE, 5)) == 5


def test_fewer_processes_than_n():
    assert top_cpu({"a": 1.0, "b": 2.0}) == ["b", "a"]


def test_report_lines():
    assert cpu_report(USAGE, 2) == ["1. batch-export 97.5%", "2. etl 55.1%"]
