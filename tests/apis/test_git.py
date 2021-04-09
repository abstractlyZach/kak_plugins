import typing
from unittest import mock

from kak_plugins.apis import git
from tests import fakes


class FakeRepo(object):
    """A fake of the PythonGit repo class"""

    def __init__(
        self,
        active_branch: typing.Optional[str] = None,
        remote_url: typing.Optional[str] = None,
    ):
        self.active_branch = active_branch
        self.remotes = {git.REMOTE: mock.MagicMock(url=remote_url)}


def test_init():
    """Raises no exceptions"""
    git.RepoApi("abc")


def test_current_branch():
    repo = git.RepoApi(FakeRepo(active_branch="mybranch"))
    assert repo.current_branch == "mybranch"


def test_remote_ssh_url():
    repo = git.RepoApi(
        FakeRepo(remote_url="git@github.com:abstractlyZach/kak_plugins.git")
    )
    assert repo.github_url == "https://github.com/abstractlyZach/kak_plugins"


def test_remote_https_url():
    repo = git.RepoApi(
        FakeRepo(remote_url="https://github.com/abstractlyZach/kak_plugins.git")
    )
    assert repo.github_url == "https://github.com/abstractlyZach/kak_plugins"


def test_get_permalink():
    repo = git.RepoApi(
        FakeRepo(
            remote_url="git@github.com:abstractlyZach/kak_plugins.git",
            active_branch="newbranch",
        )
    )
    kak_state = fakes.FakeKakState(selection=fakes.FakeSelectionDescription("L9"))
    expected = (
        "https://github.com/abstractlyZach/kak_plugins/blob/newbranch/Makefile#L9"
    )
    assert repo.get_permalink("Makefile", kak_state) == expected
