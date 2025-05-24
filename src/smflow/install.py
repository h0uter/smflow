import os
import stat


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
