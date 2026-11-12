import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from broken import line_total, invoice_total, format_money, describe_lines


def test_half_cent_rounds_up():
    assert line_total(10, "0.0125") == Decimal("0.13"), "0.125 must round UP to 0.13"


def test_another_half_cent_rounds_up_not_to_even():
    assert line_total(5, "0.5") == Decimal("2.50")
    assert line_total(1, "0.005") == Decimal("0.01"), "0.005 must round up, not to the even digit"


def test_non_half_values_round_normally():
    assert line_total(3, "0.3333") == Decimal("1.00")
    assert line_total(7, "0.0149") == Decimal("0.10")


def test_float_noise_does_not_change_the_result():
    assert line_total(1, "1.005") == Decimal("1.01"), "build Decimals from strings, not floats"


def test_line_total_returns_decimal():
    assert isinstance(line_total(2, "1.25"), Decimal)


def test_invoice_total_sums_rounded_lines():
    lines = [(10, "0.0125"), (10, "0.0125"), (3, "0.5")]
    assert invoice_total(lines) == Decimal("1.76")


def test_format_money_two_places():
    assert format_money(Decimal("12.5")) == "$12.50"


def test_describe_lines_matches_totals():
    assert describe_lines([(10, "0.0125")]) == ["10 x 0.0125 = $0.13"]
