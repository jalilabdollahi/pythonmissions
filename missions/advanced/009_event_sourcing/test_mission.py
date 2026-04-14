import pytest, sys
sys.path.insert(0, ".")
from broken import OrderAggregate

def test_place_order():
    o = OrderAggregate("ord-001")
    o.place_order(["widget"], 99.99)
    assert o.status == "placed"
    assert o.total == 99.99
    assert o.version == 1

def test_load_history():
    o = OrderAggregate("ord-002")
    history = [
        {"type": "OrderPlaced", "items": ["gizmo"], "total": 50.0},
        {"type": "OrderShipped"},
    ]
    o.load_from_history(history)
    assert o.status == "shipped"
    assert o.version == 2
