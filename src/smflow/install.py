import logging
import os
import stat
import subprocess as sp


def install_parent_hook():
    cwd = os.getcwd()

    hook = "post-checkout"
    hook_dir = os.path.join(cwd, ".git", "hooks")

    dst = os.path.join(hook_dir, hook)

    PARENT_HOOK = "uvx smflow attach-head"

    with open(dst, "w") as dst_file:
        dst_file.write("#!/bin/bash\n")
        dst_file.write(f"echo 'Running {hook} hook in {cwd}'\n")
        dst_file.write(PARENT_HOOK)
        dst_file.write("\n")

    # Make the hook executable
    st = os.stat(dst)
    os.chmod(dst, st.st_mode | stat.S_IXUSR)

    logging.info(f"Installed '{PARENT_HOOK}' hook in '{hook_dir}'")


def install_submodule_hook():
    cwd = os.getcwd()
    count = 0
    # add hook for submodules
    hook = "post-checkout"
    hook_dirs = os.path.join(cwd, ".git", "modules")
    SUBMODULE_HOOK = "uvx smflow sync-from-local"
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
        logging.info(f"Installed '{SUBMODULE_HOOK}' hook in '{sub_hook_dir}'")

    logging.info(f"Installed {count} submodule hooks.")


def install_hooks():
    logging.info("Installing hooks.")
    install_parent_hook()
    install_submodule_hook()


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
