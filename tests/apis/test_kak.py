from typing import Dict
from unittest import mock

import pytest

from kak_plugins.apis import kak
from kak_plugins.utils import line_range


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


def test_selection_desc_str():
    input_str = "55.55,66.66"
    selection = kak.SelectionDescription(input_str)
    assert str(selection) == "L55-L66"


def test_kcr_get_makes_correct_call():
    runner_spy = mock.MagicMock()
    runner_spy.return_value.stdout = b"[]"
    runner_spy.return_value.returncode = 0
    kcr = kak.KakouneCR(runner_spy)
    kcr.get(["a", "b", "c"])
    runner_spy.assert_called_once_with(
        ["kcr", "get", "--value", "a", "--value", "b", "--value", "c"],
        capture_output=True,
    )


def test_get_success():
    def runner_stub(*args, **kwargs):
        return RunSuccessStub(b'["buffile", "18.1,22.7"]\n')

    kcr = kak.KakouneCR(runner_stub)
    result = kcr.get(["a", "b", "c"])
    assert result == ["buffile", "18.1,22.7"]


def test_get_handles_error():
    def runner_stub(*args, **kwargs):
        return RunFailureStub(b"Something has gone wrong\n")

    kcr = kak.KakouneCR(runner_stub)
    with pytest.raises(RuntimeError):
        kcr.get(["a", "b", "c"])


class FakeKcr(object):
    def __init__(self, get_dict: Dict[str, str] = None):
        self._get_dict = get_dict

    def get(self, values):
        return [self._get_dict[value] for value in values]


def test_kak_state():
    kcr = FakeKcr(
        get_dict={"buffile": "/home/kakuser/abc.txt", "selection_desc": "101.1,377.9"}
    )
    state = kak.get_state(kcr)
    assert state.buffer_path == "/home/kakuser/abc.txt"
    assert state.selection.range == line_range.LineRange(101, 377)
