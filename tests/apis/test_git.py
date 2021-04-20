import typing
from unittest import mock

import pytest

from kak_plugins.apis import git
from tests import fakes

FAKE_CONFIG = {
    "remotes": {
        "abc@git.company.com": "https://git.abc.com",
        "doge@wow.net": "https://git.doge.com/",
        "git@github.com": "https://github.com",
    }
}


class FakeRepo(object):
    """A fake of the PythonGit repo class"""

    def __init__(
        self,
        active_branch: typing.Optional[str] = None,
        remote_url: str = "",
    ):
        self.active_branch = active_branch
        self.remotes = {git.REMOTE: mock.MagicMock(url=remote_url)}


def test_init():
    """Raises no exceptions"""
    git.RepoApi(FakeRepo(), FAKE_CONFIG)


def test_current_branch():
    repo = git.RepoApi(FakeRepo(active_branch="mybranch"), dict())
    assert repo.current_branch == "mybranch"


def test_remote_ssh_url():
    repo = git.RepoApi(
        FakeRepo(remote_url="git@github.com:abstractlyZach/kak_plugins.git"),
        FAKE_CONFIG,
    )
    assert repo.github_url == "https://github.com/abstractlyZach/kak_plugins"


def test_remote_https_url():
    repo = git.RepoApi(
        FakeRepo(remote_url="https://github.com/abstractlyZach/kak_plugins.git"),
        FAKE_CONFIG,
    )
    assert repo.github_url == "https://github.com/abstractlyZach/kak_plugins"


def test_get_permalink():
    repo = git.RepoApi(
        FakeRepo(
            remote_url="git@github.com:abstractlyZach/kak_plugins.git",
            active_branch="newbranch",
        ),
        FAKE_CONFIG,
    )
    kak_state = fakes.FakeKakState(selection=fakes.FakeSelectionDescription("L9"))
    expected = (
        "https://github.com/abstractlyZach/kak_plugins/blob/newbranch/Makefile#L9"
    )
    assert repo.get_permalink("Makefile", kak_state) == expected


def test_ssh_user_not_in_config():
    with pytest.raises(RuntimeError):
        git.RepoApi(
            FakeRepo(
                remote_url="oops@doesntexist.com:abstractlyZach/kak_plugins.git",
                active_branch="newbranch",
            ),
            FAKE_CONFIG,
        )


def test_doesnt_add_an_extra_slash_if_url_ends_with_it():
    """Make sure we don't have an extra slash when assembling the URL.
    This server's URL has a trailing slash and we want to ignore it.
    """
    repo = git.RepoApi(
        FakeRepo(
            remote_url="doge@wow.net:abstractlyZach/kak_plugins.git",
            active_branch="newbranch",
        ),
        FAKE_CONFIG,
    )
    kak_state = fakes.FakeKakState(selection=fakes.FakeSelectionDescription("L9"))
    expected = (
        "https://git.doge.com/abstractlyZach/kak_plugins/blob/newbranch/Makefile#L9"
    )
    assert repo.get_permalink("Makefile", kak_state) == expected
