import os
from unittest.mock import call

import click.testing
import pytest

from kak_plugins import github_permalink


@pytest.fixture
def runner():
    return click.testing.CliRunner()


@pytest.fixture
def mock_get_github_permalink(mocker):
    return mocker.patch("kak_plugins.github_permalink.get_github_permalink")


def test_main_exits_zero(runner, mock_get_github_permalink):
    result = runner.invoke(github_permalink.main)
    assert result.exit_code == 0


def test_main_exits_nonzero_on_error(runner, mock_get_github_permalink):
    mock_get_github_permalink.side_effect = Exception
    result = runner.invoke(github_permalink.main)
    assert result.exit_code != 0


def test_calls_body_with_clipboard_arg(runner, mock_get_github_permalink):
    runner.invoke(github_permalink.main, ["--clipboard-command", "my-clipboard"])
    assert mock_get_github_permalink.call_args == call("my-clipboard")


@pytest.mark.parametrize("clipboard_command", ["cool-clipboard", "pbcopy", "clippo"])
def test_calls_body_with_env_clipboard(
    runner, mock_get_github_permalink, mocker, clipboard_command
):
    mocker.patch.dict(os.environ, {"CLIPBOARD": clipboard_command})
    runner.invoke(github_permalink.main)
    assert mock_get_github_permalink.call_args == call(clipboard_command)


def test_raise_error_when_no_clipboard_env(runner, mock_get_github_permalink, mocker):
    replacement_dict = {
        key: value for key, value in os.environ.items() if key != "CLIPBOARD"
    }
    mocker.patch.dict(os.environ, replacement_dict, clear=True)
    result = runner.invoke(github_permalink.main)
    assert result.exit_code != 0
    assert isinstance(result.exception, RuntimeError)
