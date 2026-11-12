import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import broken


def test_measure_plain_argument():
    assert broken.measure("project") == 7


def test_measure_keeps_spaces_inside_one_argument():
    assert broken.measure("my report.txt") == 13, "a space must not split the argument"


def test_measure_does_not_interpret_semicolons():
    assert broken.measure("a;b") == 3, "';' is data, not a command separator"


def test_measure_many_keeps_each_argument_whole():
    assert broken.measure_many(["my file", "x", "two  spaces"]) == [7, 1, 11]


def test_measure_many_empty_list():
    assert broken.measure_many([]) == []


def test_measure_inline_with_a_quote():
    assert broken.measure_inline("it's") == 4, "user text must not be pasted into source code"


def test_measure_inline_with_code_looking_text():
    text = "')); import os; print('x"
    assert broken.measure_inline(text) == len(text)
