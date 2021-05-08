import abc


class RunnerResult(abc.ABC):
    """Store the output of a command"""

    @property
    @abc.abstractmethod
    def stdout(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def returncode(self) -> int:
        pass


class Runner(abc.ABC):
    """Handle the execution of code run outside of Python.

    The simplest candidate is subprocess.run, but this interface could also cover
    remote processes
    """

    @abc.abstractmethod
    def run(self, command: str) -> RunnerResult:
        pass
