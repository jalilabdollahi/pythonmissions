import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest

from broken import build_select, run_report


@pytest.fixture
def conn():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE invoices (id INTEGER, customer TEXT, status TEXT, amount INTEGER, created_at TEXT, note TEXT)")
    db.execute("CREATE TABLE customers (id INTEGER, name TEXT, region TEXT, tier TEXT)")
    rows = [
        (1, "acme", "open", 100, "2024-01-01", "50% off promo"),
        (2, "acme", "paid", 250, "2024-01-02", None),
        (3, "globex", "open", 75, "2024-01-03", "fifty off"),
        (4, "initech", "void", 10, "2024-01-04", "a_b"),
        (5, "initech", "open", 300, "2024-01-05", "axb"),
    ]
    db.executemany("INSERT INTO invoices VALUES (?,?,?,?,?,?)", rows)
    return db


def ids(rows):
    return [r[0] for r in rows]


def test_values_are_bound_as_parameters_never_inlined():
    sql, params = build_select("invoices", ["id"], where=[("customer", "eq", "x' OR '1'='1")])
    assert "x' OR" not in sql
    assert params == ["x' OR '1'='1"]


def test_unknown_identifiers_are_rejected():
    with pytest.raises(ValueError):
        build_select("invoices; DROP TABLE invoices", ["id"])
    with pytest.raises(ValueError):
        build_select("invoices", ["id, (SELECT 1)"])
    with pytest.raises(ValueError):
        build_select("invoices", ["id"], where=[("id", "like", 1)])
    with pytest.raises(ValueError):
        build_select("invoices", ["id"], order_by=[("secret", "asc")])


def test_order_direction_is_allow_listed(conn):
    assert ids(run_report(conn, "invoices", ["id"], order_by=[("amount", "DESC")])) == [5, 2, 1, 3, 4]
    assert ids(run_report(conn, "invoices", ["id"], order_by=[("amount", "asc")])) == [4, 3, 1, 2, 5]
    for evil in ("asc; DROP TABLE invoices", "ASC, (SELECT 1)", "sideways"):
        with pytest.raises(ValueError):
            build_select("invoices", ["id"], order_by=[("amount", evil)])


def test_null_comparison_uses_is_null(conn):
    rows = run_report(conn, "invoices", ["id"], where=[("note", "eq", None)])
    assert ids(rows) == [2], "= NULL never matches in SQL; use IS NULL"
    rows = run_report(conn, "invoices", ["id"], where=[("note", "ne", None)], order_by=[("id", "asc")])
    assert ids(rows) == [1, 3, 4, 5]


def test_like_wildcards_in_user_input_are_literal(conn):
    percent = run_report(conn, "invoices", ["id"], where=[("note", "contains", "50%")])
    assert ids(percent) == [1], "% typed by the user must not behave as a wildcard"
    underscore = run_report(conn, "invoices", ["id"], where=[("note", "contains", "a_b")])
    assert ids(underscore) == [4], "_ typed by the user must not match any single character"
    assert ids(run_report(conn, "invoices", ["id"], where=[("customer", "prefix", "ac")])) == [1, 2]


def test_in_list_including_empty(conn):
    rows = run_report(conn, "invoices", ["id"], where=[("status", "in", ["open", "void"])], order_by=[("id", "asc")])
    assert ids(rows) == [1, 3, 4, 5]
    assert run_report(conn, "invoices", ["id"], where=[("status", "in", [])]) == []


def test_limit_must_be_a_real_positive_integer(conn):
    for bad in ("1; DELETE FROM invoices", 0, -3, True, 2.5):
        with pytest.raises(ValueError):
            build_select("invoices", ["id"], limit=bad)
    assert len(run_report(conn, "invoices", ["id"], limit=2)) == 2
    assert build_select("invoices", ["id"], limit=10_000)[0].endswith("LIMIT 500")
    assert build_select("invoices", ["id"])[0].endswith("LIMIT 100")
