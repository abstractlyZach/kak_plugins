import collections
from collections.abc import Callable
import logging
from typing import List

from kak_plugins import interfaces

# represents a unit of work for writing to a clipboard
ClipboardJob = collections.namedtuple("ClipboardJob", ["clipboard_command", "message"])


def write_to_clipboard(runner: Callable, job: ClipboardJob) -> None:
    """Make a system call to write to a clipboard.

    args:
        - runner: a callable like subprocess.run that will make a system call
        - job: the unit of work to perform
    """
    logging.info(f"writing '{job.message}' to {job.clipboard_command}")
    runner(
        job.clipboard_command, input=job.message, text=True, check=True
    )  # noqa: S603


class Clipboard(object):
    def __init__(self, command: List[str], runner: interfaces.Runner) -> None:
        self._command = command
        self._runner = runner

    def write(self, message: str) -> None:
        """Write a message onto the clipboard"""
        logging.info(f"writing '{message}' to {self._command}")
        self._runner.pipe(self._command, message)
