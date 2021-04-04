import pytest

from kak_plugins import github_permalink


def test_single_line_range():
    line_range = github_permalink.LineRange(10, 10)
    assert str(line_range) == "L10"


def test_multiple_line_range():
    line_range = github_permalink.LineRange(7, 99)
    assert str(line_range) == "L7-L99"


def test_line_range_start_greater_than_stop():
    with pytest.raises(ValueError):
        github_permalink.LineRange(8, 7)


def test_line_range_start_less_than_one():
    with pytest.raises(ValueError):
        github_permalink.LineRange(0, 7)


def test_line_range_equality():
    assert github_permalink.LineRange(2, 8) == github_permalink.LineRange(2, 8)


def test_line_range_inequality():
    assert github_permalink.LineRange(1001, 7000) != github_permalink.LineRange(1, 2)


def test_line_range_not_equal_other_objects():
    assert github_permalink.LineRange(1, 2) != "abc"


def test_parse_single_width():
    input_str = "42.18,42.18"
    line_range = github_permalink.parse_selection_desc(input_str)
    assert line_range == github_permalink.LineRange(42, 42)


def test_parse_multiline_selection():
    input_str = "1.1,99.100"
    line_range = github_permalink.parse_selection_desc(input_str)
    assert line_range == github_permalink.LineRange(1, 99)


def test_parse_backwards_selection():
    input_str = "50.20,29.99"
    line_range = github_permalink.parse_selection_desc(input_str)
    assert line_range == github_permalink.LineRange(29, 50)
