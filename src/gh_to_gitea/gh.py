from github import Github
from github.PaginatedList import PaginatedList
from github.Repository import Repository


class GithubAPI:
    """
    Wrapper class to call the Github API.
    Requires an personal access token with repo access.

    :param access_token: The personal access token for the Github API.
    """

    def __init__(self, access_token: str) -> None:
        """
        Initialize the Github API with the access token.
        Sets the user object for the authenticated user.
        """
        self.gh = Github(access_token)
        self.user = self.gh.get_user()

    def get_repos(self) -> PaginatedList[Repository]:
        """
        Get all of the repos owned by the current user.

        :return: A list of repositories.
        """
        return self.user.get_repos(type="owner")

    def get_repo(self, repo_name: str) -> Repository:
        """
        Get a specific repository by name.

        :param repo_name: The name of the repository to get.

        :return: The repository object.
        """
        return self.user.get_repo(repo_name)
