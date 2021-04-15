import pytest

from kak_plugins.utils import os

PATHS_AND_ROOTS = {
    "/home/kak/workspace/kak_plugins/coolpath/function.py": "/home/kak/workspace/kak_plugins",
    "/home/zach/file.txt": "/home/zach",
    "/home/kak/.config/kak/kakrc": "/home/kak/.config",
}


def fake_os_path_exists(filename):
    # slice away the .git so we can match it with the roots
    if filename.endswith("/.git"):
        filename = filename[:-5]
    if filename in PATHS_AND_ROOTS.values():
        return True
    return False


@pytest.mark.parametrize("path,expected_root", PATHS_AND_ROOTS.items())
def test_get_git_root(path, expected_root):
    git_root = os.get_git_root(
        fake_os_path_exists,
        path,
    )
    assert git_root == expected_root


def test_cant_find_git_root():
    """Raise an error when the file is not part of a git project"""
    with pytest.raises(RuntimeError):
        os.get_git_root(fake_os_path_exists, "/abc/def/ghi/jkl")
