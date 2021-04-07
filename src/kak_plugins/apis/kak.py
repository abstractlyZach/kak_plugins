import json
import logging
import pipes
from typing import List

from .. import line_range


def kcr_get(values: List) -> List:
    # TODO: how do we test this???
    value_flags = [f"--value {value}" for value in values]
    args = " ".join(value_flags)
    command = f"kcr get {args}"
    logging.debug(f"running commmand: '{command}'")
    template = pipes.Template()
    template.prepend(command, ".-")
    with template.open("tempfile", "r") as pipe_outfile:
        kcr_output = pipe_outfile.read()
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
