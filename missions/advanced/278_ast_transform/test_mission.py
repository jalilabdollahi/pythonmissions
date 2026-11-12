import ast
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import Instrumenter, run_traced, transform


def test_transformed_source_compiles_and_runs():
    ns, calls = run_traced("def add(a, b):\n    return a + b\nresult = add(2, 3)\n")
    assert ns["result"] == 5
    assert calls == ["add"], "new nodes need line numbers or compile() refuses the tree"


def test_methods_are_traced_with_their_qualified_names():
    src = (
        "class Repo:\n"
        "    def save(self):\n"
        "        return 1\n"
        "    class Meta:\n"
        "        def table(self):\n"
        "            return 'repos'\n"
        "Repo().save()\n"
        "Repo.Meta().table()\n"
    )
    _, calls = run_traced(src)
    assert calls == ["Repo.save", "Repo.Meta.table"]


def test_nested_functions_are_instrumented_too():
    src = (
        "def outer():\n"
        "    def inner():\n"
        "        return 7\n"
        "    return inner()\n"
        "outer()\n"
    )
    ns, calls = run_traced(src)
    assert calls == ["outer", "outer.inner"], "the transformer must descend into function bodies"


def test_docstring_stays_the_first_statement():
    src = 'def documented():\n    "Explains things."\n    return 1\ndocumented()\n'
    ns, calls = run_traced(src)
    assert ns["documented"].__doc__ == "Explains things."
    assert calls == ["documented"]


def test_async_functions_are_instrumented():
    src = "async def job():\n    return 3\n"
    ns, calls = run_traced(src)
    import asyncio

    assert asyncio.run(ns["job"]()) == 3
    assert calls == ["job"]


def test_eq_none_becomes_is_none_and_not_eq_becomes_is_not():
    src = (
        "def check(x, y):\n"
        "    return (x == None, y != None)\n"
    )
    code, transformer = transform(src)
    assert transformer.rewritten_compares == 2
    ns = {"__trace__": lambda name: None}
    exec(code, ns)

    class AlwaysEqual:
        def __eq__(self, other):
            return True

        def __ne__(self, other):
            return False

    assert ns["check"](AlwaysEqual(), AlwaysEqual()) == (False, True), "identity checks ignore custom __eq__"
    assert ns["check"](None, 5) == (True, True)
    assert ns["check"](3, None) == (False, False)


def test_compares_inside_nested_expressions_and_chains_are_rewritten():
    src = (
        "def f(a, b):\n"
        "    return [v for v in (a, b) if v != None], 1 < a == None\n"
    )
    ns, calls = run_traced(src)
    assert ns["f"](1, None) == ([1], False)
    tree = ast.parse(src)
    t = Instrumenter()
    t.visit(tree)
    assert t.rewritten_compares == 2


def test_other_comparisons_are_left_alone():
    code, transformer = transform("x = 1 == 2\ny = 3 != 4\n")
    assert transformer.rewritten_compares == 0
    ns = {}
    exec(code, ns)
    assert ns["x"] is False and ns["y"] is True
