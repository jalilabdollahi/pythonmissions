import pytest, asyncio, sys
sys.path.insert(0, ".")
from broken import handle_request, log_request, run_concurrent

def test_handle_request():
    result = asyncio.run(handle_request("req-123"))
    assert "req-123" in result

def test_concurrent():
    results = asyncio.run(run_concurrent())
    assert len(results) == 2
    texts = " ".join(results)
    assert "req-001" in texts or "req-002" in texts
