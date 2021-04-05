import json
import logging
import pipes
from typing import List

# TODO: how do we test this???


def kcr_get(values: List) -> List:
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
