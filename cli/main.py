import typer
from typing import Optional
from typing_extensions import Annotated

from rich import print
from rich.status import Status

from cli import __version__
from .gh import GithubAPI
from .gitea import GiteaAPI

app = typer.Typer()


# Value looks useless here and it sort of is, but
# its required because typer will pass in a param
# to an option callback. This is also a command as
# a neat hack to provide `version` as a command and
# as a cli flag option `--version`
@app.command(name="version")
def version_callback(value: bool = True):
    """
    Prints version and exsits.
    """
    if value:
        print(f"gh-to-gitea version: {__version__}")
        raise typer.Exit()


@app.callback()
def cb(
    ctx: typer.Context,
    # Version must come first so that is_eager works correctly
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Print the version and exit",
        ),
    ] = None,
    # This is a pre-optimization but we collect these at the root level
    # and store them in the context object incase we add more commands
    # in the future, as they will likely also need all of the same credentials.
    gh_access_token: Annotated[
        str,
        typer.Option(
            "--gh-access-token",
            help="Access Token for Github API",
            envvar="GH_ACCESS_TOKEN",
        ),
    ] = ...,
    gh_user_name: Annotated[
        str,
        typer.Option(
            "--gh-user-name", help="Username for Github API", envvar="GH_USERNAME"
        ),
    ] = ...,
    gt_access_token: Annotated[
        str,
        typer.Option(
            "--gt-access-token",
            help="Access Token for Gitea API",
            envvar="GT_ACCESS_TOKEN",
        ),
    ] = ...,
    gt_url: Annotated[
        str,
        typer.Option("--gt-url", help="URL for the Gitea Instance", envvar="GT_URL"),
    ] = ...,
):
    """
    Mirror Github repositories to Gitea.

    Mirrors repositories under the authenticated user for Gitea.
    """
    ctx.obj = {
        "gh_access_token": gh_access_token,
        "gh_user_name": gh_user_name,
        "gt_access_token": gt_access_token,
        "gt_url": gt_url,
    }


@app.command()
def mirror(
    ctx: typer.Context,
    repo: Annotated[str, typer.Option(help="Specific repo to mirror")] = None,
):
    """
    Mirror all of the repositories from Github to Gitea.

    Optionally mirror a specific repository, useful for debugging or testing.

    Will not mirror forks.
    """
    gh_access_token = ctx.obj["gh_access_token"]
    gh_user_name = ctx.obj["gh_user_name"]
    gt_access_token = ctx.obj["gt_access_token"]
    gt_url = ctx.obj["gt_url"]

    gh = GithubAPI(gh_access_token)
    gt = GiteaAPI(gt_url, gt_access_token, gh_access_token, gh_user_name)

    with Status("Mirroring repositories"):
        for repo_to_clone in [gh.get_repo(repo)] if repo else gh.get_repos():
            print(f":eyes: Looking at repo {repo_to_clone.name}")
            if not repo_to_clone.fork:
                data = {
                    "repo_name": repo_to_clone.name,
                    "description": (
                        repo_to_clone.description
                        or f"A mirror of {repo_to_clone.name} from {
                            repo_to_clone.clone_url
                        }"
                    )[:255],
                    "clone_addr": repo_to_clone.clone_url,
                }
                if gt.does_repo_exist(data["repo_name"]):
                    print(
                        f":next_track_button: Skipping existing repo: {repo_to_clone.name}"
                    )
                    continue
                gt.create_repo(data, repo_to_clone.private)
            else:
                print(f":next_track_button: Skipping forked repo: {repo_to_clone.name}")


if __name__ == "__main__":
    app()
