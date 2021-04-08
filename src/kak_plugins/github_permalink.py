#! python
import logging
import os
import subprocess
import tempfile
from typing import Optional

import click
import git

from . import os as kak_plugins_os
from .apis import clipboard
from .apis import git as git_api
from .apis import kak

DEFAULT_LOGFILE = "github-permalink.log"

LOG_LEVELS = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "critical": logging.CRITICAL,
}


@click.command()
@click.option(
    "-c",
    "--clipboard-command",
    envvar="CLIPBOARD",
    help="Program that is used to write to the system clipboard. "
    + "CLIPBOARD will be read from the environment if this flag is not specified.",
)
@click.option(
    "-l",
    "--log-level",
    default="info",
    help="Level of information to write to the logs.",
    type=click.Choice(LOG_LEVELS),
    show_default=True,
)
@click.option(
    "-w",
    "--write-to-logfile",
    is_flag=True,
    help="If this flag is on, write to a logfile instead.",
)
@click.option("-p", "--log-path", help="Where to write the logfile.")
def main(
    log_level: str,
    write_to_logfile: bool,
    log_path: Optional[str],
    clipboard_command: Optional[str],
) -> None:  # pragma: no cover
    """Call kcr to get editor info, then parse it and write it to the clipboard"""
    # TODO: write click tests. maybe need to use a mock?
    if not clipboard_command:
        raise RuntimeError("CLIPBOARD is not set")
    if log_path:
        # if a user specifies a log path, we can assume they want to log
        write_to_logfile = True
    _setup_logging(log_level, write_to_logfile, log_path)
    get_github_permalink(clipboard_command)
    logging.info("=== script complete ===")


def _setup_logging(
    log_level: str, write_to_logfile: bool, log_path: Optional[str]
) -> None:  # pragma: no cover
    if write_to_logfile:
        if log_path is None:
            temp_dir = tempfile.gettempdir()
            log_path = f"{temp_dir}/{DEFAULT_LOGFILE}"
        logging.basicConfig(
            filename=log_path,
            format="%(levelname)s: %(message)s",
            level=LOG_LEVELS[log_level],
        )
    else:
        # write to stderr
        logging.basicConfig(
            format="%(levelname)s: %(message)s",
            level=LOG_LEVELS[log_level],
        )
    logging.info(f"log level set to {log_level.upper()}")


def get_github_permalink(clipboard_command: str) -> None:  # pragma: no cover
    # TODO: break this file up and stop ignoring coverage
    absolute_path, selection_desc = kak.kcr_get(
        subprocess.run, ["buffile", "selection_desc"]
    )
    selection = kak.SelectionDescription(selection_desc)
    git_root = kak_plugins_os.get_git_root(os.path.exists, absolute_path)
    repo = git_api.RepoApi(git.Repo(git_root))
    relative_path = os.path.relpath(absolute_path, git_root)
    permalink = repo.get_permalink(relative_path, selection.range)
    clipboard_job = clipboard.ClipboardJob(clipboard_command, permalink)
    clipboard.write_to_clipboard(subprocess.run, clipboard_job)
