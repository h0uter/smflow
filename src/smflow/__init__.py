"""
usage: smflow [-h] {attach-head,sync-from-local,install-hooks} ...

Git submodule management script.

positional arguments:
  {attach-head,sync-from-local,install-hooks}
                        Sub-command to run
    attach-head         Attaches the head of the submodules to the branch.
    sync-from-local     Updates .gitmodules from local file state.
    install-hooks       Installs the githooks.

options:
  -h, --help            show this help message and exit
"""

import argparse
import os
import stat
import subprocess as sp

from git import Repo


def main():
    parser = argparse.ArgumentParser(
        description="Make the flow of working with Git submodules smoother."
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="command to run"
    )

    subparsers.add_parser(
        "attach-head",
        help="Attaches the head of the submodules to the branch and reset to the commit-sha.",
    )

    subparsers.add_parser(
        "sync-from-local", help="Updates .gitmodules from local file state."
    )

    subparsers.add_parser("install-hooks", help="Installs the githooks.")
    args = parser.parse_args()

    match args.command:
        case "attach-head":
            reattach_submodule_heads_to_branch()
        case "sync-from-local":
            update_branch_setting_in_dotgitmodules_from_local()
        case "install-hooks":
            install_hooks()
        case _:
            raise ValueError(f"Unknown command: {args.command}")


def install_parent_hook():
    cwd = os.getcwd()

    hook = "post-checkout"
    hook_dir = os.path.join(cwd, ".git", "hooks")

    dst = os.path.join(hook_dir, hook)

    PARENT_HOOK = "uv run python main.py attach-head"

    with open(dst, "w") as dst_file:
        dst_file.write("#!/bin/bash\n")
        dst_file.write(f"echo 'Running {hook} hook in {cwd}'\n")
        dst_file.write(PARENT_HOOK)
        dst_file.write("\n")

    # Make the hook executable
    st = os.stat(dst)
    os.chmod(dst, st.st_mode | stat.S_IXUSR)

    print(f"Installed '{PARENT_HOOK}' hook in '{hook_dir}'")
    print()


def install_submodule_hook():
    cwd = os.getcwd()
    count = 0
    # add hook for submodules
    hook = "post-checkout"
    hook_dirs = os.path.join(cwd, ".git", "modules")
    SUBMODULE_HOOK = "uv run python ../main.py sync-from-local"
    for submodule in os.listdir(hook_dirs):
        sub_hook_dir = os.path.join(hook_dirs, submodule, "hooks")

        # Copy the hooks to the submodule's hooks directory
        dst = os.path.join(sub_hook_dir, hook)
        with open(dst, "w") as dst_file:
            dst_file.write("#!/bin/bash\n")
            dst_file.write(f"echo 'Running {hook} hook in {cwd}'\n")
            dst_file.write(SUBMODULE_HOOK)
            dst_file.write("\n")

        # Make the hook executable
        st = os.stat(dst)
        os.chmod(dst, st.st_mode | stat.S_IXUSR)
        count += 1
        print(f"Installed '{SUBMODULE_HOOK}' hook in '{sub_hook_dir}'")

    print(f"Installed {count} submodule hooks.")


def install_hooks():
    print("Installing hooks.")
    install_parent_hook()
    install_submodule_hook()


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


if __name__ == "__main__":
    main()
