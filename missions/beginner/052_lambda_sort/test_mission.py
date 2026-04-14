import os, sys
sys.path.insert(0, os.path.dirname(__file__))

SERVERS = [{"name":"web-01","cpu_pct":75},{"name":"api-01","cpu_pct":20},{"name":"db-01","cpu_pct":90}]

def test_sorted_by_cpu():
    from broken import sort_by_cpu
    result = sort_by_cpu(SERVERS)
    assert result[0]["cpu_pct"] == 20
    assert result[-1]["cpu_pct"] == 90

def test_returns_all():
    from broken import sort_by_cpu
    assert len(sort_by_cpu(SERVERS)) == 3
