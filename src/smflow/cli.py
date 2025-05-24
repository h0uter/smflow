"""
usage: smflow [-h] {init,install-hooks,configure-git,attach-head,sync-from-local} ...

Make the flow of working with Git submodules smoother.

positional arguments:
  {init,install-hooks,configure-git,attach-head,sync-from-local}
                        command to run
    init                Setup all functionality of smflow.
    install-hooks       Installs the githooks.
    configure-git       Configures some ergonomics for git submodules.
    attach-head         Attaches the head of the submodules to the branch and reset to the commit-sha.
    sync-from-local     Updates .gitmodules from local file state.

options:
  -h, --help            show this help message and exit
"""

import argparse

from smflow.hooks import (
    reattach_submodule_heads_to_branch,
    update_branch_setting_in_dotgitmodules_from_local,
)
from smflow.install import configure_git, init_submodules, install_hooks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Make the flow of working with Git submodules smoother."
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="command to run"
    )

    # install commands
    subparsers.add_parser("init", help="Setup all functionality of smflow.")
    subparsers.add_parser("install-hooks", help="Installs the githooks.")
    subparsers.add_parser(
        "configure-git", help="Configures some ergonomics for git submodules."
    )

    # hooks commands
    subparsers.add_parser(
        "attach-head",
        help="Attaches the head of the submodules to the branch and reset to the commit-sha.",
    )
    subparsers.add_parser(
        "sync-from-local", help="Updates .gitmodules from local file state."
    )

    args = parser.parse_args()

    match args.command:
        # install
        case "init":
            install_hooks()
            configure_git()
            init_submodules()
        case "install-hooks":
            install_hooks()
        case "configure-git":
            configure_git()

        # hooks
        case "attach-head":
            reattach_submodule_heads_to_branch()
        case "sync-from-local":
            update_branch_setting_in_dotgitmodules_from_local()

        case _:
            raise ValueError(f"Unknown command: {args.command}")
