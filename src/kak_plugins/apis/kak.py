import json
import pipes
from typing import List

# TODO: how do we test this???


def kcr_get(values: List) -> List:
    value_flags = [f"--value {value}" for value in values]
    args = " ".join(value_flags)
    template = pipes.Template()
    template.prepend(f"kcr get {args}", ".-")
    with template.open("tempfile", "r") as pipe_outfile:
        kcr_output = pipe_outfile.read()
    return json.loads(kcr_output)
