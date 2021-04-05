#! python
import logging
import os
import tempfile

import git

from . import line_range
from .apis import clipboard
from .apis import git as git_api
from .apis import kak

LOGFILE_NAME = "github-permalink.log"


def main() -> None:
    """Call kcr to get editor info, then parse it and write it to the clipboard"""
    tempdir = tempfile.gettempdir()
    logging.basicConfig(
        filename=tempdir + "/" + LOGFILE_NAME,
        format="%(levelname)s:%(message)s",
        level=logging.DEBUG,
    )
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
