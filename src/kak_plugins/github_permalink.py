#! python
import collections
import os
import sys
import typing

import git

from .apis import git as git_api


class LineRange(object):
    """Describes a range of lines"""

    def __init__(self, start: int, stop: int):
        if stop < start:
            # LineRanges are dumb objects and should always have start/stop ordered
            raise ValueError(f"Invalid range. {stop} < {start}")
        if start < 1:
            # kakoune and github start their line counts at 1
            raise ValueError(f"Invalid range start. {start} < 0")
        self._start = start
        self._stop = stop

    def __str__(self):
        if self._start == self._stop:
            return f"L{self._start}"
        else:
            return f"L{self._start}-L{self._stop}"

    def __eq__(self, other):
        return self._start, self._stop == other._start, other._stop


def main():
    # read from pipe
    for line in sys.stdin:
        path, selection_desc = _parse_kak_output(line)
        permalink = get_permalink(path, selection_desc)
        print(permalink)


def _parse_kak_output(kak_output: str) -> typing.Tuple[str]:
    """Parse the output of `kcr get --value buffile --value selection_desc`
    into path and selection_desc
    """
    stripped_output = kak_output.lstrip('["').rstrip('"]')
    return stripped_output.split('","')


def get_permalink(path, selection_desc):
    repo = git_api.RepoApi(git.Repo("."))
    branch = repo.get_current_branch()
    base_url = repo.get_github_url()
    line_range = parse_selection_desc(selection_desc)
    relative_path = _convert_to_relative_path(path)
    return _assemble_permalink(base_url, branch, relative_path, line_range)


def parse_selection_desc(selection_desc: str) -> LineRange:
    """Parse a selction description from kakoune into a LineRange"""
    anchor_pos, cursor_pos = selection_desc.split(",")
    anchor_line = int(anchor_pos.split(".")[0])
    cursor_line = int(cursor_pos.split(".")[0])
    return LineRange(min(anchor_line, cursor_line), max(anchor_line, cursor_line))


def _convert_to_relative_path(path: str) -> str:
    """Convert an absolute or relative path to its relative path"""
    return os.path.relpath(path, os.getcwd())


def _assemble_permalink(base_url: str, branch: str, path: str, line_range: LineRange):
    return f"{base_url}/blob/{branch}/{path}#{line_range}"
