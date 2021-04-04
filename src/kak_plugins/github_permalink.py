#! python
import os

import git

from .apis import clipboard
from .apis import git as git_api
from .apis import kak


class LineRange(object):
    """Describes a range of lines"""

    def __init__(self, start: int, stop: int) -> None:
        if stop < start:
            # LineRanges are dumb objects and should always have start/stop ordered
            raise ValueError(f"Invalid range. {stop} < {start}")
        if start < 1:
            # kakoune and github start their line counts at 1
            raise ValueError(f"Invalid range start. {start} < 1")
        self._start = start
        self._stop = stop

    def __str__(self) -> str:
        if self._start == self._stop:
            return f"L{self._start}"
        else:
            return f"L{self._start}-L{self._stop}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LineRange):
            return (self._start, self._stop) == (other._start, other._stop)
        return False


def main() -> None:
    absolute_path, selection_desc = kak.kcr_get(["buffile", "selection_desc"])
    permalink = get_permalink(absolute_path, selection_desc)
    clipboard_command = clipboard.get_clipboard_command()
    clipboard.write_to_clipboard(permalink, clipboard_command)


def get_permalink(absolute_path: str, selection_desc: str) -> str:
    repo = git_api.RepoApi(git.Repo("."))
    branch = repo.get_current_branch()
    base_url = repo.get_github_url()
    line_range = parse_selection_desc(selection_desc)
    relative_path = os.path.relpath(absolute_path, os.getcwd())
    return f"{base_url}/blob/{branch}/{relative_path}#{line_range}"


def parse_selection_desc(selection_desc: str) -> LineRange:
    """Parse a selction description from kakoune into a LineRange"""
    anchor_pos, cursor_pos = selection_desc.split(",")
    anchor_line = int(anchor_pos.split(".")[0])
    cursor_line = int(cursor_pos.split(".")[0])
    return LineRange(min(anchor_line, cursor_line), max(anchor_line, cursor_line))
