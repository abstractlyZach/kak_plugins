from collections.abc import Callable
import json
import logging
from typing import List, NamedTuple, Optional

from kak_plugins.utils import line_range


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


class KakouneState(NamedTuple):
    """Internal representation of Kakoune's state

    This is a canonical list of everything we care about. I'll need to explore
    other options if this ever becomes too big of a list. However, there doesn't
    seem to be any huge overhead from getting multiple values from kcr
    """

    buffer_path: str
    selection: SelectionDescription


class KakouneExpansion(NamedTuple):
    """Information from Kakoune that we can query

    https://github.com/mawww/kakoune/blob/master/doc/pages/expansions.asciidoc
    """

    # kakoune's name for the expansion
    expansion_name: str
    # converts the expansion if it can be turned into something more useful than a string
    parser: Optional[Callable]
    # our internal name for the state
    state_name: str
    # TODO: add type if we want to query expansions that aren't values in the future


EXPANSIONS = [
    KakouneExpansion(expansion_name="buffile", parser=None, state_name="buffer_path"),
    KakouneExpansion(
        expansion_name="selection_desc",
        parser=SelectionDescription,
        state_name="selection",
    ),
]


def get_state(kcr: KakouneCR) -> KakouneState:
    """Call kcr to get the current state of Kakoune.

    Requests all expansions in EXPANSIONS and parses them to get nice
    python objects.
    """
    expansion_values = kcr.get([expansion.expansion_name for expansion in EXPANSIONS])
    parsed_values = dict()
    for expansion_definition, value in zip(EXPANSIONS, expansion_values):
        state_name = expansion_definition.state_name
        if expansion_definition.parser is None:
            parsed_values[state_name] = value
        else:
            parsed_values[state_name] = expansion_definition.parser(value)
        logging.debug(f'{state_name} is "{parsed_values[state_name]}"')
    return KakouneState(**parsed_values)
