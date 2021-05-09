from collections.abc import Callable
import os
import subprocess
from typing import List

from kak_plugins import interfaces


def get_git_root(path_exists_function: Callable, current_path: str) -> str:
    """Find the absolute path of the given path's git root"""
    # Traverse up the directory tree until we find a directory
    # that contains a .git directory
    while not path_exists_function(f"{current_path}/.git"):
        if current_path == "/":
            raise RuntimeError(f"{current_path} is not in a git directory")
        current_path = os.path.dirname(current_path)
    return current_path


class SubprocessRunner(interfaces.Runner):
    def run(self, command: List[str]) -> str:
        """Execute a command as a subprocess

        Successful commands have their stdout returned. Unsuccessful commands
        have their stderr raised as a RuntimeError.
        """
        # this command gets flagged as a security risk. We're not worried about code injection
        # since this code should only get run by source code inside this project
        result = subprocess.run(command, capture_output=True)  # noqa: S603
        if result.returncode != 0:
            error_message = str(result.stderr, encoding="utf-8").strip()
            raise RuntimeError(f"Command {command} failed: {error_message}")
        return str(result.stdout, "utf-8").strip()
