import logging

import git

from .. import line_range

REMOTE = "origin"
URL_REPLACEMENTS = {"git@github.com:": "https://github.com/"}


class RepoApi(object):
    """wrapper class for git.Repo"""

    def __init__(self, repo: git.Repo) -> None:
        self._repo = repo

    @property
    def current_branch(self) -> str:
        """Return the current local git branch"""
        return str(self._repo.active_branch)

    @property
    def github_url(self) -> str:
        """Convert an https or ssh remote into a github url"""
        remote_url = self._repo.remotes[REMOTE].url
        # if we have an ssh remote, convert it to a URL
        for ssh_login in URL_REPLACEMENTS:
            if remote_url.startswith(ssh_login):
                logging.debug(f"Remote URL starts with ssh_login: {remote_url}")
                remote_url = remote_url.lstrip(ssh_login)
                remote_url = URL_REPLACEMENTS[ssh_login] + remote_url
        remote_url = remote_url.rstrip(".git")
        return remote_url

    def get_permalink(
        self, path_from_git_root: str, range: line_range.LineRange
    ) -> str:
        """Create a permalink for the editor's selection"""
        return (
            f"{self.github_url}/blob/{self.current_branch}/{path_from_git_root}#{range}"
        )
