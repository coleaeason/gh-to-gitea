import requests
import json

from rich import print


class GiteaAPI:
    """
    A wrapper around Gitea API to create mirror repositories.

    Requires github information in order to create the mirrors
    """

    def __init__(
        self,
        gitea_url: str,
        gitea_api_token: str,
        github_token: str,
        github_username: str,
    ) -> None:
        """
        Initialize the Gitea API with the given information.
        Sets the session instance for the API.
        Sets the username for the authenticated user.

        :param gitea_url: The URL for the Gitea instance.
        :param gitea_api_token: The API token for Gitea.
        :param github_token: The token for the Github API.
        :param github_username: The username for the Github API.
        """
        self.url = f"{gitea_url}/api/v1"
        self.token = gitea_api_token
        self.github_token = github_token
        self.github_username = github_username
        self.session = self._get_session()
        self.username = self.get_user()["login"]

    def _get_session(self) -> requests.Session:
        """
        Internal function to get a session for Gitea.
        """
        session = requests.Session()
        session.headers.update(
            {
                "Content-type": "application/json",
                "Authorization": f"token {self.token}",
            }
        )

        return session

    def get_user(self) -> dict:
        """
        Returns the user JSON from the authenticated Gitea user.
        """
        r = self.session.get(f"{self.url}/user")
        return r.json()

    def create_repo(self, data: object, isPrivate: bool) -> None:
        """
        Create a repository on Gitea with the given data.

        If the repository already exists, it will not create it.

        :param data: The data to create the repository with.
            Certain values might be overwritten.
        :param isPrivate: If the repository is private or not.
        """
        if isPrivate:
            data["auth_username"] = self.github_username
            data["auth_password"] = self.github_token

        data["service"] = "github"
        data["wiki"] = True
        data["auth_token"] = self.github_token
        data["mirror"] = True

        jsonstring = json.dumps(data)
        r = self.session.post(f"{self.url}/repos/migrate", data=jsonstring)

        if r.status_code == 201:
            print(f":sparkles: Success: Repository {data['repo_name']} Created")
        elif r.status_code == 409:
            print(f":warning: Warning: Repository {data['repo_name']} Already Exists")
        else:
            print(r.status_code, r.text, jsonstring)

    def does_repo_exist(self, repo_name: str) -> bool:
        """
        Check if a repository exists on Gitea.

        :param repo_name: The name of the repository to check.

        :returns: True if the repository exists, False otherwise.
        """
        r = self.session.get(f"{self.url}/repos/{self.username}/{repo_name}")
        return r.status_code == 200
