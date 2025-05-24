# smflow

Tools and git hooks to make it easier to work with submodules are updated frequently, enable a sort of virtual mono repo.

## Usage

> requires `uv` to be installed

Install with `uv tool install smflow`

Then from your parent project with submodules run:

```bash
smflow init
```

## Details

`smflow init` will:

### Git hooks

- Automatically attach heads and reset submodules to the correct commit when you checkout a branch in the parent repository.
- Automatically update `.gitmodules` when you change branches in the children.

### Git submodule settings

`smflow` wil set the following git settings:

```bash
git config submodule.recurse true
```

To automatically checkout the submodules when you change branch in the parent.

```bash
git config push.recurseSubmodules on-demand
```

To automatically push changes in children when you try to push parent repository, and it references child commits that are not present on their origin yet (only works if parent and child have identical branch names). Otherwise, it will warn you and suggest first pushing the child repository.

## Notes

- smflow does not currently support recursive submodules, i.e. submodules inside submodules.
