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

from smflow.hooks import (
    reattach_submodule_heads_to_branch,
    update_branch_setting_in_dotgitmodules_from_local,
)
from smflow.install import install_hooks


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
