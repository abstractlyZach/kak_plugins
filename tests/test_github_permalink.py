from kak_plugins import github_permalink


def test_single_line_permalink():
    permalink = github_permalink.get_permalink(
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
    permalink = github_permalink.get_permalink(
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
