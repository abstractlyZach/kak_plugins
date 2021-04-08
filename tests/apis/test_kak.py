from unittest import mock

from kak_plugins import line_range
from kak_plugins.apis import kak


class RunnerStub(object):
    def __init__(self, output):
        self._output = output

    def __call__(self, *args, **kwargs):
        return RunResultStub(self._output)


class RunResultStub(object):
    def __init__(self, output):
        self._output = output

    @property
    def stdout(self):
        return self._output


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


def test_kcr_get_correct_call():
    runner_spy = mock.MagicMock()
    runner_spy.return_value.stdout = b"[]"
    kak.kcr_get(runner_spy, ["a", "b", "c"])
    runner_spy.assert_called_once_with(
        ["kcr", "get", "--value", "a", "--value", "b", "--value", "c"],
        capture_output=True,
        check=True,
    )


def test_kcr_get_gets_processed_correctly():
    runner_stub = RunnerStub(b'["buffile", "18.1,22.7"]\n')
    result = kak.kcr_get(runner_stub, ["a", "b", "c"])
    assert result == ["buffile", "18.1,22.7"]
