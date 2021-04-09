from unittest import mock

import pytest

from kak_plugins import line_range
from kak_plugins.apis import kak


class RunSuccessStub(object):
    def __init__(self, output):
        self._output = output

    @property
    def stdout(self):
        return self._output

    @property
    def returncode(self):
        return 0


class RunFailureStub(object):
    def __init__(self, err_message, exit_code=1):
        self._err_message = err_message
        self._exit_code = exit_code

    @property
    def stderr(self):
        return self._err_message

    @property
    def returncode(self):
        return self._exit_code


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
    runner_spy.return_value.returncode = 0
    kcr = kak.KakouneCR(runner_spy)
    kcr.kcr_get(["a", "b", "c"])
    runner_spy.assert_called_once_with(
        ["kcr", "get", "--value", "a", "--value", "b", "--value", "c"],
        capture_output=True,
    )


def test_kcr_get_gets_processed_correctly():
    def runner_stub(*args, **kwargs):
        return RunSuccessStub(b'["buffile", "18.1,22.7"]\n')

    kcr = kak.KakouneCR(runner_stub)
    result = kcr.kcr_get(["a", "b", "c"])
    assert result == ["buffile", "18.1,22.7"]


def test_kcr_get_handles_error():
    def runner_stub(*args, **kwargs):
        return RunFailureStub(b"Something has gone wrong\n")

    kcr = kak.KakouneCR(runner_stub)

    with pytest.raises(RuntimeError):
        kcr.kcr_get(["a", "b", "c"])
