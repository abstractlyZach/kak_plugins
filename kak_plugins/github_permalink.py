#! python

import sys
import collections


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


def parse_selection_desc(selection_desc: str) -> LineRange:
    """Parse a selction description from kakoune into a LineRange"""
    anchor_pos, cursor_pos = selection_desc.split(",")
    anchor_line = int(anchor_pos.split(".")[0])
    cursor_line = int(cursor_pos.split(".")[0])
    return LineRange(min(anchor_line, cursor_line), max(anchor_line, cursor_line))


def get_permalink(base_url: str, branch: str, path: str, line_range: LineRange):
    return f"{base_url}/blob/{branch}/{path}#{line_range}"


if __name__ == "__main__":
    # read from pipe
    for line in sys.stdin:
        line_range = get_line_range(line)
        print(get_permalink(line_range))
