import os
from collections.abc import Callable


def get_git_root(path_exists_function: Callable, path: str) -> str:
    import logging

    logging.info("getting git root")
    while not path_exists_function(f"{path}/.git"):
        logging.info("loop")
        if path == "/":
            raise RuntimeError(f"{path} is not in a git directory")
        path = os.path.dirname(path)
    return path
