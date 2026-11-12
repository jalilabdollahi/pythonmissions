import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decimal import Decimal

import broken


def test_half_cents_round_up():
    assert broken.money(Decimal("0.125")) == Decimal("0.13"), "invoices round half up, not half to even"
    assert broken.money(Decimal("0.135")) == Decimal("0.14")


def test_line_cost_is_rounded_to_cents():
    assert broken.line_cost("0.0825", 1000) == Decimal("82.50")
    assert broken.line_cost("0.125", 1) == Decimal("0.13")


def test_total_is_the_sum_of_the_printed_lines():
    rows, total = broken.invoice([("a", "0.125", 1), ("b", "0.125", 1), ("c", "0.125", 1)])
    assert [cost for _, cost in rows] == [Decimal("0.13")] * 3
    assert total == Decimal("0.39"), "customers add up the rounded lines"


def test_total_keeps_two_decimals_for_empty_invoice():
    rows, total = broken.invoice([])
    assert rows == []
    assert total == Decimal("0.00")


def test_discount_percentage_is_exact():
    assert broken.apply_discount(Decimal("100.00"), 5.025) == Decimal("94.98")
    assert broken.apply_discount(Decimal("100.00"), "5.025") == Decimal("94.98")


def test_simple_discount():
    assert broken.apply_discount(Decimal("80.00"), 25) == Decimal("60.00")


def test_share_of_total_uses_decimal_percentages():
    rows = [("a", Decimal("1.00")), ("b", Decimal("3.00"))]
    assert broken.share_of_total(rows, Decimal("4.00")) == {"a": Decimal("25.0"), "b": Decimal("75.0")}
    assert broken.share_of_total([], Decimal("0.00")) == {}


def test_team_totals_and_render():
    totals = broken.team_totals({"search": [("vm", "1.10", 3)], "ml": [("gpu", "2.5125", 2)]})
    assert totals == {"search": Decimal("3.30"), "ml": Decimal("5.03")}
    text = broken.render([("vm", Decimal("3.30"))], Decimal("3.30"))
    assert text.splitlines() == ["vm" + " " * 16 + "3.30", "TOTAL" + " " * 13 + "3.30"]
