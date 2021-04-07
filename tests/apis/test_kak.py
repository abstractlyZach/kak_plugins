from kak_plugins import line_range
from kak_plugins.apis import kak


def test_parse_single_width():
    input_str = "42.18,42.18"
    selection = kak.SelectionDescription(input_str)
    assert selection.range == line_range.LineRange(42, 42)


def test_parse_multiline_selection():
    input_str = "1.1,99.100"
    selection = kak.SelectionDescription(input_str)
    assert selection.range == line_range.LineRange(1, 99)


def test_parse_backwards_selection():
    input_str = "50.20,29.99"
    selection = kak.SelectionDescription(input_str)
    assert selection.range == line_range.LineRange(29, 50)
