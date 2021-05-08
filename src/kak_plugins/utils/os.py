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
        try:
            result = subprocess.run(  # noqa: S603
                command, capture_output=True, check=True
            )
        except subprocess.CalledProcessError:
            raise RuntimeError(f"Command {command} failed.")
        return str(result.stdout, "utf-8").strip()
