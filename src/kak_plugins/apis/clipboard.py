import collections
from collections.abc import Callable
import logging

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
