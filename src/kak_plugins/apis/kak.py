from collections.abc import Callable
import json
import logging
from typing import List

from .. import line_range


class KakouneCR(object):
    """Handles all calls to kakoune.cr"""

    def __init__(self, runner: Callable) -> None:
        """Stores a Callable that has the interface of subprocess.run()"""
        self._runner = runner

    def get(self, values: List[str]) -> List:
        """Query kakoune for information about itself

        This link contains the possible values to query
        https://github.com/mawww/kakoune/blob/master/doc/pages/expansions.asciidoc#value-expansions

        For more info on the command: https://github.com/alexherbo2/kakoune.cr#get
        """
        kcr_command = ["kcr", "get"]
        for value in values:
            kcr_command.append("--value")
            kcr_command.append(value)
        logging.debug(f"running commmand: '{kcr_command}'")
        result = self._runner(kcr_command, capture_output=True)
        if result.returncode != 0:
            error_message = str(result.stderr, encoding="utf-8").strip()
            raise RuntimeError(f"kakoune.cr: {error_message}")
        else:
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

    def __str__(self) -> str:
        return str(self._line_range)


class KakouneState(object):
    """A representation of Kakoune's state

    Takes information from kcr and turns it into internal representations
    that should be easier to work with than pure strings
    """

    def __init__(self, kcr: KakouneCR) -> None:
        """Use kcr to query and parse the editor's state"""
        self._state = dict()
        parsers = {"buffile": None, "selection_desc": SelectionDescription}
        kak_states = kcr.get(parsers)
        for state, state_name, parser in zip(
            kak_states, parsers.keys(), parsers.values()
        ):
            if parser is not None:
                self._state[state_name] = parser(state)
            else:
                self._state[state_name] = state

    # there's gotta be a better way than defining a property for each one, right?
    @property
    def buffile(self) -> str:
        return self._state["buffile"]

    @property
    def selection(self) -> SelectionDescription:
        return self._state["selection_desc"]
