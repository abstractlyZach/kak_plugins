import git

REMOTE = "origin"
URL_REPLACEMENTS = {"git@github.com:": "https://github.com/"}


class RepoApi(object):
    """wrapper class for git.Repo"""

    def __init__(self, repo: git.Repo):
        self._repo = repo

    def get_current_branch(self) -> str:
        """Return the current local git branch"""
        return str(self._repo.active_branch)

    def get_github_url(self) -> str:
        """Convert an https or ssh remote into a github url"""
        remote_url = self._repo.remotes[REMOTE].url
        # if we have an ssh remote, convert it to a URL
        for ssh_login in URL_REPLACEMENTS:
            if remote_url.startswith(ssh_login):
                remote_url = remote_url.lstrip(ssh_login)
                remote_url = URL_REPLACEMENTS[ssh_login] + remote_url
        remote_url = remote_url.rstrip('.git')
        return remote_url
