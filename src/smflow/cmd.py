from enum import Enum


class Cmd(str, Enum):
    INIT = "init"
    INSTALL_HOOKS = "install-hooks"
    CONFIGURE_GIT = "configure-git"
    ATTACH_HEADS = "attach-heads"
    SYNC_FROM_LOCAL = "sync-from-local"

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}.{self.name}"
