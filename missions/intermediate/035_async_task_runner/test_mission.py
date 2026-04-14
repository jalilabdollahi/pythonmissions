import pytest
import asyncio
import sys
sys.path.insert(0, ".")
from broken import run_checks, main

def test_run_checks():
    services = ["api", "db", "cache"]
    results = main(services)
    assert len(results) == 3
    assert all(r["status"] == "ok" for r in results)

def test_all_services_present():
    results = main(["web", "worker"])
    names = [r["service"] for r in results]
    assert "web" in names
    assert "worker" in names
