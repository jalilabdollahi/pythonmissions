import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


GOOD = "Tr1cky-Passw0rd"


def test_good_password_has_no_problems():
    assert broken.check_password(GOOD, "alice") == []
    assert broken.is_valid(GOOD, "alice")


def test_password_of_exactly_min_length_is_long_enough():
    pw = "Abcdefgh12!?"
    assert len(pw) == 12
    assert "too_short" not in broken.check_password(pw), "'at least 12' includes 12"


def test_one_character_below_min_length_is_too_short():
    assert broken.check_password("Abcdefg12!?")[0] == "too_short"


def test_space_is_not_a_symbol():
    assert broken.check_password("Abcdefgh 1234") == ["no_symbol"]


def test_character_class_codes_in_order():
    assert broken.check_password("12345678901234") == ["no_lower", "no_upper", "no_symbol"]
    assert broken.check_password("abcdefghijklmn") == ["no_upper", "no_digit", "no_symbol"]


def test_username_is_checked_ignoring_case():
    assert "contains_username" in broken.check_password("xxALICExx1!abcdE", "alice")
    assert "contains_username" in broken.check_password("xxaliceXX1!abcdE", "ALICE")


def test_empty_username_never_matches():
    assert "contains_username" not in broken.check_password(GOOD, "")


def test_custom_min_length_and_explain():
    assert broken.check_password("Ab1!", min_length=4) == []
    assert broken.explain(["too_short", "no_digit"]) == "use more characters; add a digit"
    assert broken.explain([]) == "ok"
