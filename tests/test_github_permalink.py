import pytest
from kak_plugins import github_permalink


def test_single_line_permalink():
    permalink = github_permalink._assemble_permalink(
        "https://github.com/abstractlyZach/kak_plugins",
        "main",
        "poetry.lock",
        github_permalink.LineRange(1, 1),
    )
    assert (
        permalink
        == "https://github.com/abstractlyZach/kak_plugins/blob/main/poetry.lock#L1"
    )


def test_range_permalink():
    permalink = github_permalink._assemble_permalink(
        "https://github.com/abstractlyZach/kak_plugins",
        "main",
        "test/test_github_permalink.py",
        github_permalink.LineRange(1, 5),
    )
    assert (
        permalink
        == "https://github.com/abstractlyZach/kak_plugins"
        + "/blob/main/test/test_github_permalink.py#L1-L5"
    )


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

def test_parse_kak_output():
    expected_path =  "/home/zach/workspace/kak_plugins/kak_plugins/github_permalink.py"
    expected_selection_desc = "41.1,41.1"
    output = f'["{expected_path}","{expected_selection_desc}"]'
    path, selection_desc = github_permalink._parse_kak_output(output)
    assert path == expected_path
    assert selection_desc == expected_selection_desc

