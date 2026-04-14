import pytest, sys
sys.path.insert(0, ".")
from broken import QueryOptimizer

STATS = {"users": 1000000, "orders": 50000, "products": 500}

def test_predicate_pushdown():
    opt = QueryOptimizer(STATS)
    query = {
        "from": "main",
        "joins": {"users": {}, "orders": {}},
        "where": [
            {"table": "users", "col": "status", "val": "active"},
            {"col": "date", "val": "2024"},
        ]
    }
    result = opt.push_predicates(query)
    assert len(result["where"]) == 1  # only unpushable remains
    assert result["joins"]["users"]["conditions"][0]["col"] == "status"

def test_join_reorder():
    opt = QueryOptimizer(STATS)
    query = {"joins": {"users": {}, "products": {}, "orders": {}}}
    result = opt.reorder_joins(query)
    keys = list(result["joins"].keys())
    assert keys[0] == "products"  # smallest (500) first
