import logging
import os
import subprocess as sp

from git import Repo


def update_branch_setting_in_dotgitmodules_from_local():
    """
    Updates the branch setting for the current submodule in the parent repository's .gitmodules file
    based on the local branch state.

    This function determines the current working directory (assumed to be the submodule's directory),
    detects the current Git branch, and updates the corresponding `branch` entry in the parent
    repository's .gitmodules file for this submodule. If the submodule is in a detached HEAD state,
    the function prints a message and exits without making changes.

    Raises:
        subprocess.CalledProcessError: If the git commands fail.
    """
    logging.info("Updating .gitmodules from local file state.")

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
        logging.warning(f"Submodule {cwd} is in a detached HEAD state.")
        return

    logging.info(f"Submodule {cwd} is on branch {current_branch}.")

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
    """
    Reattaches the HEADs of all submodules in the current repository to the commit referenced by the parent repository,
    and checks out the corresponding branch for each submodule.

    For each submodule:
        - Determines the commit hash that the parent repository references.
        - Reads the configured branch for the submodule.
        - Checks out the branch in the submodule.
        - Resets the submodule's HEAD to the commit referenced by the parent repository.

    This ensures that each submodule is on the correct branch and at the exact commit specified by the parent repository.
    """
    repo = Repo(".")

    for sm in repo.submodules:
        subrepo: Repo = sm.module()

        path = sm.path

        # Get the commit hash the parent repo is pointing to
        entry = repo.head.commit.tree / path
        submodule_commit_hash = entry.hexsha

        with sm.config_reader() as cr:
            branch = cr.get_value("branch")

        logging.info(f"{sm.name} {sm.url} {sm.path} {branch}")

        subrepo.git.checkout(branch)

        subrepo.git.reset("--hard", submodule_commit_hash)
