# smflow

Tools and git hooks to make it easier to work with submodules are updated frequently, enable a sort of virtual mono repo.

## Usage

Install with `uv tool install smflow`

Then from your project with submodules run:

`smflow install-hooks`

To install the git hooks.

For the best experience set the following git settings:

```bash
git config submodule.recurse true
```

To automatically checkout the submodules when you change branch in the parent.

```bash
git config push.recurseSubmodules on-demand
```

To automatically push changes in children when you try to push parent repository and it references child commits that are not present on their origin yet (only works if parent and child have identical branch names). Otherwise, it will warn you and suggest first pushing the child repository.
