import pytest, sys
sys.path.insert(0, ".")
from broken import SagaOrchestrator

def test_success_path():
    saga = SagaOrchestrator()
    saga.step("payment", lambda ctx: "charged", lambda ctx: None)
    saga.step("inventory", lambda ctx: "reserved", lambda ctx: None)
    result = saga.execute({})
    assert result["payment"] == "charged"
    assert result["inventory"] == "reserved"

def test_compensation_reverse_order():
    order = []
    saga = SagaOrchestrator()
    saga.step("step1", lambda ctx: "ok1", lambda ctx: order.append("comp1"))
    saga.step("step2", lambda ctx: "ok2", lambda ctx: order.append("comp2"))
    saga.step("step3", lambda ctx: (_ for _ in ()).throw(RuntimeError("fail")),
              lambda ctx: order.append("comp3"))
    with pytest.raises(RuntimeError):
        saga.execute({})
    assert order == ["comp2", "comp1"]
