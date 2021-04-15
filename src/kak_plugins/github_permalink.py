#! python
import logging
import os
import subprocess
import sys
from typing import Optional

import click
import git

from kak_plugins.apis import clipboard
from kak_plugins.apis import git as git_api
from kak_plugins.apis import kak
from kak_plugins.utils import os as kak_plugins_os

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
def main(verbosity_level: int, clipboard_command: Optional[str]) -> None:
    """Call kcr to get editor info, then parse it and write it to the clipboard"""
    if not clipboard_command:
        raise RuntimeError("CLIPBOARD is not set")
    # print this many levels of the traceback when errors occur
    sys.tracebacklimit = verbosity_level
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=VERBOSITY_LOG_LEVELS[verbosity_level],
    )
    get_github_permalink(clipboard_command)


def get_github_permalink(clipboard_command: str) -> None:  # pragma: no cover
    # TODO: break this file up and stop ignoring coverage
    kcr = kak.KakouneCR(subprocess.run)
    kak_state = kak.get_state(kcr)
    git_root = kak_plugins_os.get_git_root(os.path.exists, kak_state.buffer_path)
    repo = git_api.RepoApi(git.Repo(git_root))
    relative_path = os.path.relpath(kak_state.buffer_path, git_root)
    permalink = repo.get_permalink(relative_path, kak_state)
    clipboard_job = clipboard.ClipboardJob(clipboard_command, permalink)
    clipboard.write_to_clipboard(subprocess.run, clipboard_job)
