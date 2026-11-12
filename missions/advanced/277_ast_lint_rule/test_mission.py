import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import format_findings, lint_source


def codes(source):
    return [(f.line, f.col) for f in lint_source(source)]


def test_blocking_call_in_async_function_is_reported_with_its_own_line():
    src = (
        "import time\n"
        "\n"
        "async def poll():\n"
        "    x = 1\n"
        "    time.sleep(2)\n"
    )
    findings = lint_source(src)
    assert [(f.line, f.col, f.code) for f in findings] == [(5, 5, "ASYNC100")]
    assert "asyncio.sleep" in findings[0].message


def test_multi_line_call_is_reported_where_it_starts():
    src = (
        "import subprocess\n"
        "async def build():\n"
        "    subprocess.run(\n"
        "        ['make'],\n"
        "        check=True,\n"
        "    )\n"
    )
    assert codes(src) == [(3, 5)]


def test_same_call_in_sync_function_is_fine():
    src = "import time\ndef slow():\n    time.sleep(1)\n"
    assert lint_source(src) == []


def test_calls_nested_inside_other_calls_are_visited():
    src = (
        "import requests, json\n"
        "async def fetch(u):\n"
        "    return json.loads(requests.get(u).text)\n"
    )
    assert codes(src) == [(3, 23)], "generic_visit is what descends into arguments"


def test_sync_helper_defined_inside_async_function_is_not_flagged():
    src = (
        "import time\n"
        "async def main(loop):\n"
        "    def worker():\n"
        "        time.sleep(1)\n"
        "    await loop.run_in_executor(None, worker)\n"
        "    await loop.run_in_executor(None, lambda: time.sleep(1))\n"
        "    time.sleep(3)\n"
    )
    assert codes(src) == [(7, 5)], "only the direct call blocks the loop; helpers run in a thread"


def test_async_function_nested_in_sync_function_is_flagged_again():
    src = (
        "import time\n"
        "def outer():\n"
        "    async def inner():\n"
        "        time.sleep(1)\n"
    )
    assert codes(src) == [(4, 9)]


def test_import_aliases_are_resolved():
    src = (
        "import time as t\n"
        "from time import sleep as nap\n"
        "from subprocess import run\n"
        "import requests as rq\n"
        "async def go():\n"
        "    t.sleep(1)\n"
        "    nap(1)\n"
        "    run(['ls'])\n"
        "    rq.post('http://x')\n"
    )
    assert codes(src) == [(6, 5), (7, 5), (8, 5), (9, 5)]


def test_unrelated_names_and_syntax_errors():
    src = "async def go(sleep, obj):\n    sleep(1)\n    obj.time.sleep(1)\n"
    assert lint_source(src) == []
    bad = lint_source("async def go(:\n    pass\n")
    assert len(bad) == 1 and bad[0].code == "E999" and bad[0].line == 1
    out = format_findings(lint_source("import time\nasync def f():\n    time.sleep(1)\n"), "svc.py")
    assert out == ["svc.py:3:5: ASYNC100 time.sleep() blocks the event loop; use asyncio.sleep"]
