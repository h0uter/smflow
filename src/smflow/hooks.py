import os
import subprocess as sp

from git import Repo


def update_branch_setting_in_dotgitmodules_from_local():
    print("Updating .gitmodules from local file state.")

    cwd = os.path.basename(os.getcwd())

    current_branch = (
        sp.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=sp.DEVNULL,
        )
        .decode()
        .strip()
    )

    if current_branch == "HEAD":
        print(f"Submodule {cwd} is in a detached HEAD state.")
        return

    print(f"Submodule {cwd} is on branch {current_branch}.")

    sp.run(
        [
            "git",
            "config",
            "-f",
            "../.gitmodules",
            f"submodule.{cwd}.branch",
            current_branch,
        ],
        check=True,
    )


def reattach_submodule_heads_to_branch():
    repo = Repo(".")

    for sm in repo.submodules:
        subrepo: Repo = sm.module()

        path = sm.path

        # Get the commit hash the parent repo is pointing to
        entry = repo.head.commit.tree / path
        submodule_commit_hash = entry.hexsha

        with sm.config_reader() as cr:
            branch = cr.get_value("branch")

        print(sm.name, sm.url, sm.path, branch)

        subrepo.git.checkout(branch)

        subrepo.git.reset("--hard", submodule_commit_hash)
