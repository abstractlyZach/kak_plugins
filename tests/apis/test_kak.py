from typing import Dict, List

import pytest

from kak_plugins import interfaces
from kak_plugins.apis import kak
from kak_plugins.utils import line_range


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


class RunnerSuccessStub(interfaces.Runner):
    def __init__(self, stdout):
        self._std_out = stdout

    def run(self, command: List[str]):
        return self._std_out


class RunnerFailureStub(interfaces.Runner):
    def __init__(self, exception_class):
        self._exception_class = exception_class

    def run(self, command: List[str]):
        raise self._exception_class()


def test_get_success():
    runner = RunnerSuccessStub('["buffile", "18.1,22.7"]')
    kcr = kak.KakouneCR(runner)
    result = kcr.get(["a", "b", "c"])
    assert result == ["buffile", "18.1,22.7"]


def test_get_handles_error():
    runner = RunnerFailureStub(RuntimeError)
    kcr = kak.KakouneCR(runner)
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
