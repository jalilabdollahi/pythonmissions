import os, sys
sys.path.insert(0, os.path.dirname(__file__))

SERVERS = [{"name":"web-01","cpu_pct":45},{"name":"db-01","cpu_pct":92},{"name":"api-01","cpu_pct":60}]

def test_first_is_highest():
    from broken import top_cpu
    result = top_cpu(SERVERS)
    assert result[0]["cpu_pct"] == 92

def test_last_is_lowest():
    from broken import top_cpu
    result = top_cpu(SERVERS)
    assert result[-1]["cpu_pct"] == 45
