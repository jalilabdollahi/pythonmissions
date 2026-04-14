import pytest, sys
sys.path.insert(0, ".")
from broken import RunbookExecutor

def test_all_success():
    r = RunbookExecutor()
    r.add_step("step1", lambda ctx: "done1")
    r.add_step("step2", lambda ctx: "done2")
    result = r.execute({})
    assert len(result["steps"]) == 2

def test_stop_on_failure():
    r = RunbookExecutor()
    r.add_step("step1", lambda ctx: (_ for _ in ()).throw(RuntimeError("fail")))
    r.add_step("step2", lambda ctx: "done2")
    result = r.execute({})
    assert result["success"] is False
    assert len(result["steps"]) == 1  # stopped after step1

def test_continue_on_error():
    r = RunbookExecutor()
    r.add_step("step1", lambda ctx: (_ for _ in ()).throw(RuntimeError("warn")), continue_on_error=True)
    r.add_step("step2", lambda ctx: "done2")
    result = r.execute({})
    assert len(result["steps"]) == 2
