#! python
import logging
import os
import tempfile
from typing import Optional

import click
import git

from . import line_range
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
    default="critical",
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
    repo = git_api.RepoApi(git.Repo("."))
    relative_path = os.path.relpath(absolute_path, os.getcwd())
    line_range = parse_selection_desc(selection_desc)
    permalink = repo.get_permalink(relative_path, line_range)
    clipboard_command = clipboard.get_clipboard_command()
    clipboard.write_to_clipboard(permalink, clipboard_command)


def parse_selection_desc(selection_desc: str) -> line_range.LineRange:
    """Parse a selction description from kakoune into a LineRange"""
    anchor_pos, cursor_pos = selection_desc.split(",")
    anchor_line = int(anchor_pos.split(".")[0])
    cursor_line = int(cursor_pos.split(".")[0])
    logging.debug(f"anchor at {anchor_line}; cursor at {cursor_line}")
    return line_range.LineRange(
        min(anchor_line, cursor_line), max(anchor_line, cursor_line)
    )
