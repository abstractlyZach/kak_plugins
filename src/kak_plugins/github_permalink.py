#! python
import logging
import os
import subprocess
from typing import Optional

import click
import git

from . import os as kak_plugins_os
from .apis import clipboard
from .apis import git as git_api
from .apis import kak

DEFAULT_LOGFILE = "github-permalink.log"

# maps from verbosity level to log levels
VERBOSITY_LOG_LEVELS = {
    0: logging.WARNING,
    1: logging.INFO,
    2: logging.DEBUG,
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
    "-v",
    "--verbose",
    "verbosity_level",
    default=0,
    count=True,
    help="Set verbosity. Add more v's to increase verbosity. For example, -v is "
    + "verbosity level 1 and -vv is verbosity level 2",
)
def main(
    verbosity_level: int, clipboard_command: Optional[str]
) -> None:  # pragma: no cover
    """Call kcr to get editor info, then parse it and write it to the clipboard"""
    # TODO: write click tests. maybe need to use a mock?
    if not clipboard_command:
        raise RuntimeError("CLIPBOARD is not set")
    _setup_logging(verbosity_level)
    get_github_permalink(clipboard_command)
    logging.info("=== script complete ===")


def _setup_logging(verbosity_level: int) -> None:  # pragma: no cover
    log_level = VERBOSITY_LOG_LEVELS[verbosity_level]
    # writes to stderr
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=log_level,
    )


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
