# Github to Gitea
gh-to-gitea is a simple cli tool to mirror all of your Github repos to a Gitea instance. If a repo already exists, it is skipped. The mirror setting in Gitea keeps the repos in sync using webhook events once configured, so you only need to mirror a repo once.

## How to use
You can close this repo and run it locally with `uv`:
```
$ uv run gh-to-gitea
 Usage: gh-to-gitea [OPTIONS] COMMAND [ARGS]...

 Mirror Github repositories to Gitea.
 Mirrors repositories under the authenticated user for Gitea.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --gh-access-token           TEXT  Access Token for Github API [env var: GH_ACCESS_TOKEN] [default: None] [required]                           │
│ *  --gh-user-name              TEXT  Username for Github API [env var: GH_USERNAME] [default: None] [required]                                   │
│ *  --gt-access-token           TEXT  Access Token for Gitea API [env var: GT_ACCESS_TOKEN] [default: None] [required]                            │
│ *  --gt-url                    TEXT  URL for the Gitea Instance [env var: GT_URL] [default: None] [required]                                     │
│    --install-completion              Install completion for the current shell.                                                                   │
│    --show-completion                 Show completion for the current shell, to copy it or customize the installation.                            │
│    --help                            Show this message and exit.                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ version   Prints version and exsits.                                                                                                             │
│ mirror    Mirror all of the repositories from Github to Gitea.                                                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

You can also specify a single repo to mirror:
```
uv run gh-to-gitea mirror repo-name
```