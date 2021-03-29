#! python

import sys
import collections


class LineRange(object):
    def __init__(self, start: int, stop: int):
        self._start = start
        self._stop = stop

    def __str__(self):
        if self._start == self._stop:
            return f"L{self._start}"
        else:
            return f"L{self._start}-L{self._stop}"


def get_line_range(selection_desc: str):
    pass


def get_permalink(base_url: str, branch: str, path: str, line_range: LineRange):
    return f"{base_url}/blob/{branch}/{path}#{line_range}"


if __name__ == "__main__":
    for line in sys.stdin:
        line_range = get_line_range(line)
        print(get_permalink(line_range))
