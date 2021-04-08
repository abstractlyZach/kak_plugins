import json
import logging
from collections.abc import Callable
from typing import List

from .. import line_range


def kcr_get(runner: Callable, values: List) -> List:
    kcr_command = ["kcr", "get"]
    for value in values:
        kcr_command.append("--value")
        kcr_command.append(value)
    logging.debug(f"running commmand: '{kcr_command}'")
    result = runner(kcr_command, capture_output=True, check=True)
    kcr_output = str(result.stdout, encoding="utf-8").strip()
    logging.debug(f"kcr output: {kcr_output}")
    return json.loads(kcr_output)


class SelectionDescription(object):
    def __init__(self, selection_desc: str) -> None:
        """Parse a selction description from kakoune"""
        anchor_pos, cursor_pos = selection_desc.split(",")
        anchor_line = int(anchor_pos.split(".")[0])
        cursor_line = int(cursor_pos.split(".")[0])
        logging.debug(f"anchor at {anchor_line}; cursor at {cursor_line}")
        self._line_range = line_range.LineRange(
            min(anchor_line, cursor_line), max(anchor_line, cursor_line)
        )

    @property
    def range(self) -> line_range.LineRange:
        return self._line_range
