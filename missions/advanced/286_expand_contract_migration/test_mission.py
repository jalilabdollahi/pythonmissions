import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import (
    add_column,
    backfill,
    drop_column,
    dual_write,
    render_report,
    switch_reads,
    validate_plan,
)


def rename_plan():
    return [
        add_column("patients", "display_name", nullable=True),
        dual_write("patients", "display_name"),
        backfill("patients", "display_name"),
        switch_reads("patients", "display_name"),
        drop_column("patients", "fullname", replaced_by="display_name"),
    ]


def indexes(steps):
    return [i for i, _ in validate_plan(steps)]


def test_canonical_rename_is_safe():
    assert validate_plan(rename_plan()) == []
    assert "safe" in render_report(rename_plan())


def test_not_null_column_without_default_is_rejected():
    steps = [add_column("patients", "mrn", nullable=False)]
    assert indexes(steps) == [0], "old app versions cannot insert into a required column"


def test_not_null_with_default_is_allowed():
    steps = [add_column("patients", "tier", nullable=False, default="standard")]
    assert validate_plan(steps) == [], "a default makes NOT NULL safe for old writers"


def test_backfill_must_wait_for_dual_writes():
    plan = rename_plan()
    plan[1], plan[2] = plan[2], plan[1]
    assert indexes(plan) == [1], "backfill before dual writes loses rows written in between"


def test_cannot_drop_before_reads_switch():
    plan = rename_plan()
    del plan[3]
    assert indexes(plan) == [3]
    assert "dropped before reads" in render_report(plan)


def test_progress_on_one_table_does_not_excuse_another():
    steps = [
        add_column("orders", "region", nullable=True),
        dual_write("orders", "region"),
        backfill("orders", "region"),
        add_column("invoices", "region", nullable=True),
        switch_reads("invoices", "region"),
    ]
    assert indexes(steps) == [4], "invoices.region was never backfilled"


def test_unknown_operations_are_reported():
    steps = [{"op": "truncate", "table": "t", "column": "c"}]
    assert indexes(steps) == [0]
