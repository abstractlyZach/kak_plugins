import logging
from typing import Dict

import git

from kak_plugins.apis import kak

REMOTE = "origin"


class RepoApi(object):
    """wrapper class for git.Repo"""

    def __init__(self, repo: git.Repo, configuration: Dict) -> None:
        self._repo = repo
        self._config = configuration
        logging.debug(f"config is {self._config}")

    @property
    def current_branch(self) -> str:
        """Return the current local git branch"""
        return str(self._repo.active_branch)

    @property
    def github_url(self) -> str:
        """Convert an https or ssh remote into a github url"""
        remote_url = self._repo.remotes[REMOTE].url
        # if we have an ssh remote, convert it to a URL
        for ssh_login in self._config["remotes"]:
            if remote_url.startswith(ssh_login):
                logging.debug(f"Remote URL starts with ssh_login: {remote_url}")
                ssh_user, repo_path = remote_url.split(":")
                base_url = self._config["remotes"][ssh_login]
                if not base_url.endswith("/"):
                    base_url += "/"
                remote_url = base_url + repo_path
        remote_url = remote_url.rstrip(".git")
        return remote_url

    def get_permalink(
        self, path_from_git_root: str, kak_state: kak.KakouneState
    ) -> str:
        """Create a permalink for the editor's selection"""
        return (
            f"{self.github_url}/blob/{self.current_branch}/"
            + f"{path_from_git_root}#{kak_state.selection}"
        )
