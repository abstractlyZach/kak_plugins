from kak_plugins import github_permalink
from kak_plugins import line_range


def test_parse_single_width():
    input_str = "42.18,42.18"
    parsed_line_range = github_permalink.parse_selection_desc(input_str)
    assert parsed_line_range == line_range.LineRange(42, 42)


def test_parse_multiline_selection():
    input_str = "1.1,99.100"
    parsed_line_range = github_permalink.parse_selection_desc(input_str)
    assert parsed_line_range == line_range.LineRange(1, 99)


def test_parse_backwards_selection():
    input_str = "50.20,29.99"
    parsed_line_range = github_permalink.parse_selection_desc(input_str)
    assert parsed_line_range == line_range.LineRange(29, 50)
