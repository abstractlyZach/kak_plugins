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
        self._set_github_url()
        logging.debug(f"config is {self._config}")

    def _set_github_url(self) -> None:
        """Convert an https or ssh remote into a github url"""
        remote_url = self._repo.remotes[REMOTE].url
        if "@" in remote_url:
            logging.debug(f"Remote URL is an ssh URL: {remote_url}")
            remote_url = self._get_github_url(remote_url)
        remote_url = remote_url.rstrip(".git")
        self._github_url = remote_url

    @property
    def current_branch(self) -> str:
        """Return the current local git branch"""
        return str(self._repo.active_branch)

    @property
    def github_url(self) -> str:
        """Return the GitHub URL to this repo"""
        return self._github_url

    def _get_github_url(self, remote_url: str) -> str:
        # if we have an ssh remote, convert it to a URL
        for ssh_login, url_replacement in self._config["remotes"].items():
            if remote_url.startswith(ssh_login):
                logging.debug(f"Remote URL starts with ssh_login: {ssh_login}")
                return _convert_ssh_remote_to_github_url(remote_url, url_replacement)
        else:
            raise RuntimeError("Could not find SSH to URL conversion in config: {}")

    def get_permalink(
        self, path_from_git_root: str, kak_state: kak.KakouneState
    ) -> str:
        """Create a permalink for the editor's selection"""
        return (
            f"{self.github_url}/blob/{self.current_branch}/"
            + f"{path_from_git_root}#{kak_state.selection}"
        )


def _convert_ssh_remote_to_github_url(remote_url: str, github_base_url: str) -> str:
    ssh_user, repo_path = remote_url.split(":")
    if not github_base_url.endswith("/"):
        github_base_url += "/"
    return github_base_url + repo_path
