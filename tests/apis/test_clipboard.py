import subprocess
from unittest import mock

import pytest

from kak_plugins.apis import clipboard


def test_clipboard_runs_with_correct_args():
    runner_spy = mock.MagicMock()
    job = clipboard.ClipboardJob("wl-copy", "writing this to my clipboard")
    clipboard.write_to_clipboard(runner_spy, job)
    runner_spy.assert_called_once_with(
        "wl-copy", input="writing this to my clipboard", text=True, check=True
    )


def test_error_raised_correctly():
    raised_exception = subprocess.CalledProcessError(returncode=1, cmd="abc")
    runner_fake = mock.MagicMock(side_effect=raised_exception)
    job = clipboard.ClipboardJob("wl-copy", "writing this to my clipboard")
    with pytest.raises(subprocess.CalledProcessError):
        clipboard.write_to_clipboard(runner_fake, job)
