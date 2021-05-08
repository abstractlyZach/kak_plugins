import abc
from typing import List


class Runner(abc.ABC):
    """Handle the execution of code run outside of Python.

    The simplest candidate is subprocess.run, but this interface could also cover
    remote processes
    """

    @abc.abstractmethod
    def run(self, command: List[str]) -> str:
        pass
