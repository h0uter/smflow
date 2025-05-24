import logging
import os
import stat
import subprocess as sp
from pathlib import Path

HOOK_SHELL = "/bin/sh"
HOOK = "post-checkout"
PARENT_HOOK = "uvx smflow attach-head"
SUBMODULE_HOOK = "uvx smflow sync-from-local"


def install_hook(dst: Path, hook: str):
    with open(dst, "w") as dst_file:
        dst_file.write(f"#!{HOOK_SHELL}\n")
        dst_file.write(f"echo 'Running '{hook}''\n")
        dst_file.write(hook)
        dst_file.write("\n")

    # Make the hook executable
    st = os.stat(dst)
    os.chmod(dst, st.st_mode | stat.S_IXUSR)

    logging.info(f"Installed '{hook}' hook in '{dst}'")


def install_parent_hook(hook: str, hook_type: str = HOOK):
    cwd = os.getcwd()
    hook_dir = os.path.join(cwd, ".git", "hooks")
    dst = os.path.join(hook_dir, hook_type)

    install_hook(dst, hook)


def install_submodule_hook(hook: str, hook_type: str = HOOK):
    cwd = os.getcwd()
    hook_dirs = os.path.join(cwd, ".git", "modules")

    dsts: list[Path] = []
    for submodule in os.listdir(hook_dirs):
        sub_hook_dir = os.path.join(hook_dirs, submodule, "hooks")

        # Copy the hooks to the submodule's hooks directory
        dst = os.path.join(sub_hook_dir, hook_type)
        install_hook(dst, hook)
        dsts.append(dst)

    logging.info(f"Installed {len(dsts)} submodule hooks.")


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
