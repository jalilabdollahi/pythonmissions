import pytest, sys
sys.path.insert(0, ".")
from broken import instrument_code

def test_instrument_compiles():
    code = """
def greet(name):
    return f"Hello, {name}"
"""
    compiled = instrument_code(code)
    assert compiled is not None

def test_instrumented_runs():
    code = """
def add(a, b):
    return a + b
result = add(2, 3)
"""
    compiled = instrument_code(code)
    ns = {}
    exec(compiled, ns)
    assert ns["result"] == 5
