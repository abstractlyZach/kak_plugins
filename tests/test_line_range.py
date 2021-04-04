import pytest

from kak_plugins import line_range


def test_single_line_range():
    lr = line_range.LineRange(10, 10)
    assert str(lr) == "L10"


def test_multiple_line_range():
    lr = line_range.LineRange(7, 99)
    assert str(lr) == "L7-L99"


def test_line_range_start_greater_than_stop():
    with pytest.raises(ValueError):
        line_range.LineRange(8, 7)


def test_line_range_start_less_than_one():
    with pytest.raises(ValueError):
        line_range.LineRange(0, 7)


def test_line_range_equality():
    assert line_range.LineRange(2, 8) == line_range.LineRange(2, 8)


def test_line_range_inequality():
    assert line_range.LineRange(1001, 7000) != line_range.LineRange(1, 2)


def test_line_range_not_equal_other_objects():
    assert line_range.LineRange(1, 2) != "abc"
