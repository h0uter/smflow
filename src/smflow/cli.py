import argparse

from smflow.cmd import Cmd
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
    subparsers.add_parser(Cmd.INIT, help="Setup all functionality of smflow.")
    subparsers.add_parser(Cmd.INSTALL_HOOKS, help="Installs the githooks.")
    subparsers.add_parser(
        Cmd.CONFIGURE_GIT,
        help="Configures some ergonomic settings for git submodules in local `.gitconfig`.",
    )

    # hooks commands
    subparsers.add_parser(
        Cmd.ATTACH_HEADS,
        help="Attaches the head of the submodules to the branch and reset to the commit-sha.",
        description="doc:" + reattach_submodule_heads_to_branch.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers.add_parser(
        Cmd.SYNC_FROM_LOCAL,
        help="Updates .gitmodules from local file state.",
        description="doc:" + update_branch_setting_in_dotgitmodules_from_local.__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    args = parser.parse_args()

    match args.command:
        # install
        case Cmd.INIT:
            init_submodules()
            install_hooks()
            configure_git()
        case Cmd.INSTALL_HOOKS:
            install_hooks()
        case Cmd.CONFIGURE_GIT:
            configure_git()

        # hooks
        case Cmd.ATTACH_HEADS:
            reattach_submodule_heads_to_branch()
        case Cmd.SYNC_FROM_LOCAL:
            update_branch_setting_in_dotgitmodules_from_local()

        case _:
            raise ValueError(f"Unknown command: {args.command}")
