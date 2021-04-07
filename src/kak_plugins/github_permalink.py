#! python
import logging
import os
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
    "-l",
    "--log-level",
    default="info",
    help="Level of information to write to the logs.",
    type=click.Choice(LOG_LEVELS),
)
@click.option("-p", "--log-path", help="Where to write the logfile.")
def main(log_level: str, log_path: Optional[str]) -> None:
    """Call kcr to get editor info, then parse it and write it to the clipboard"""
    _setup_logging(log_level, log_path)
    get_github_permalink()
    logging.info("=== script complete ===")


def _setup_logging(log_level: str, log_path: Optional[str]) -> None:  # pragma: no cover
    if log_path is None:
        temp_dir = tempfile.gettempdir()
        log_path = f"{temp_dir}/{DEFAULT_LOGFILE}"
    logging.basicConfig(
        filename=log_path,
        format="%(levelname)s: %(message)s",
        level=LOG_LEVELS[log_level],
    )
    logging.info(f"log level set to {log_level.upper()}")


def get_github_permalink() -> None:
    absolute_path, selection_desc = kak.kcr_get(["buffile", "selection_desc"])
    selection = kak.SelectionDescription(selection_desc)
    git_root = kak_plugins_os.get_git_root(os.path.exists, absolute_path)
    repo = git_api.RepoApi(git.Repo(git_root))
    relative_path = os.path.relpath(absolute_path, git_root)
    permalink = repo.get_permalink(relative_path, selection.range)
    clipboard_command = clipboard.get_clipboard_command()
    clipboard.write_to_clipboard(permalink, clipboard_command)
