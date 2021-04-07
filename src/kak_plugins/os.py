import os
from collections.abc import Callable


def get_git_root(path_exists_function: Callable, current_path: str) -> str:
    """Find the absolute path of the given path's git root"""
    # Traverse up the directory tree until we find a directory
    # that contains a .git directory
    while not path_exists_function(f"{current_path}/.git"):
        if current_path == "/":
            raise RuntimeError(f"{current_path} is not in a git directory")
        current_path = os.path.dirname(current_path)
    return current_path
