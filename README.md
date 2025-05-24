[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://pre-commit.com)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![image](https://img.shields.io/pypi/v/smflow.svg)](https://pypi.python.org/pypi/smflow)

# Git Submodule Flow (`smflow`)

**smflow** is a lightweight toolset and set of Git hooks designed to make working with Git submodules significantly easier. It helps keep submodules in sync with the parent repository, enabling a "virtual monorepo" workflow — without giving up the benefits of repository modularity.

---

## 🚀 Features

- Intuitively work with submodules through VS Code git interface.
- Automatically attaches submodule `HEAD`s to the commits referenced by the parent repository.
- Quickly see how many changes the current submodule is behind the tracked branch.
- Keeps local submodules in sync when switching branches in the parent project.
- Automatically update `.gitmodules` in parent when changing locally checking out branches for submodules.
- Configures Git for a smoother submodule experience:
  - Auto-checkout submodules on branch change
  - Auto-push submodule commits when pushing the parent

---

## 📦 Installation

> **Note**: Requires [`uv`](https://github.com/astral-sh/uv) to be installed.

Install smflow with:

```bash
uv tool install smflow
```

## 🛠️ Usage

From the root of your parent repository (the one that contains submodules), run:

```bash
smflow init
```

This will configure your repository with the appropriate Git settings and install the necessary hooks.

For help and available commands, run: `smflow --help`:

```
usage: smflow [-h]
              {init,install-hooks,configure-git,attach-heads,sync-from-local}
              ...

Make the flow of working with Git submodules smoother.

positional arguments:
  {init,install-hooks,configure-git,attach-heads,sync-from-local}
                        command to run
    init                Setup all functionality of smflow.
    install-hooks       Installs the githooks.
    configure-git       Configures some ergonomic settings for git submodules
                        in local `.gitconfig`.
    attach-heads        Attaches the head of the submodules to the branch and
                        reset to the commit-sha.
    sync-from-local     Updates .gitmodules from local file state.

options:
  -h, --help            show this help message and exit
```

## 🔍 What smflow init Does

### 🔗 Git Hooks

The following hooks will be installed:

- Post-checkout hook

Automatically resets submodules to the correct commit when you checkout a branch in the parent repository.

- Post-branch-change hook

Updates .gitmodules when you switch between branches, ensuring consistency across the repo.

### ⚙️ Git Configuration

smflow sets these recommended Git config values:

```bash
git config submodule.recurse true
```

Ensures submodules are automatically checked out when switching branches.

```bash
git config push.recurseSubmodules on-demand
```

Allows pushing submodule commits automatically when pushing the parent repository — if the submodules and parent share the same branch name. If not, Git will warn and suggest pushing submodules first.

## ⚠️ Limitations

- smflow does not currently support recursive submodules, i.e. submodules within submodules.

## 🧩 Why smflow?

Managing submodules manually is tedious and error-prone. smflow minimizes the overhead and makes it easier to:

- Stay in sync with your team
- Avoid detached HEAD states in submodules
- Prevent pushing parent branches that reference unpublished submodule commits

Whether you’re working with multiple shared libraries or simply trying to tame Git submodules, smflow provides a smoother, safer workflow.
