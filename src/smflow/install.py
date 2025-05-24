import logging
import os
import stat
import subprocess as sp
from pathlib import Path

from smflow.cmd import Cmd

HOOK_SHELL = "/bin/sh"
HOOK = "post-checkout"
PARENT_HOOK = f"smflow {Cmd.ATTACH_HEADS}"
SUBMODULE_HOOK = f"smflow {Cmd.SYNC_FROM_LOCAL}"


def _install_hook(destination: Path, hook: str):
    with open(destination, "w") as hook_file:
        hook_file.write(f"#!{HOOK_SHELL}\n")
        hook_file.write(f"echo 'Running '{hook}''\n")
        hook_file.write(hook)
        hook_file.write("\n")

    # Make the hook executable
    st = os.stat(destination)
    os.chmod(destination, st.st_mode | stat.S_IXUSR)

    logging.info(f"Installed '{hook}' hook in '{destination}'")


def install_parent_hook(hook: str, hook_type: str = HOOK):
    cwd = Path.cwd()
    hook_dir = cwd / ".git" / "hooks"
    destination = hook_dir / hook_type

    _install_hook(destination, hook)


def install_submodule_hook(hook: str, hook_type: str = HOOK):
    cwd = Path.cwd()
    submodules = cwd / ".git" / "modules"

    destinations: list[Path] = []
    for submodule in submodules.iterdir():
        submodule_hook_dir = submodules / submodule / "hooks"

        # Copy the hooks to the submodule's hooks directory
        destination = submodule_hook_dir / hook_type
        _install_hook(destination, hook)
        destinations.append(destination)

    logging.info(f"Installed {len(destinations)} submodule hooks.")


def install_hooks():
    logging.info("Installing hooks.")
    install_parent_hook(PARENT_HOOK)
    install_submodule_hook(SUBMODULE_HOOK)


def configure_git() -> None:
    """Configure some ergonomics for git submodules."""
    try:
        sp.run(
            ["git", "config", "--local", "submodule.recurse", "true"],
            check=True,
        )
        logging.info(
            "Automatically recurse into submodules when running git commands. Automatically checks out submodules when changing branches in the parent repository."
        )
    except sp.CalledProcessError as e:
        print(f"Failed to configure git setting: {e}")

    try:
        sp.run(
            ["git", "config", "--local", "push.recurseSubmodules", "on-demand"],
            check=True,
        )
        logging.info(
            "Automatically push submodules when pushing the parent repository. This will only push submodules that have been modified."
        )
    except sp.CalledProcessError as e:
        print(f"Failed to configure git setting: {e}")


def init_submodules() -> None:
    """Initialize the submodule."""
    try:
        sp.run(["git", "submodule", "update", "--init", "--recursive"], check=True)
        logging.info("Submodule initialized.")
    except sp.CalledProcessError as e:
        print(f"Failed to initialize submodule: {e}")
