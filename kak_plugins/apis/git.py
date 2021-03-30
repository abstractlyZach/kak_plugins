import git

REMOTE = "origin"


class Repo(object):
    """wrapper class for git.Repo"""

    def __init__(self, repo: git.Repo):
        self._repo = repo

    def get_current_branch(self) -> str:
        return str(self._repo.active_branch)

    def get_github_url(self) -> str:
        return self._repo.remotes[REMOTE].url
