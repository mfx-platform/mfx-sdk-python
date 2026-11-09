from enum import Enum


class TerminalOperationChangedKind(str, Enum):
    ATTACH = "attach"
    DETACH = "detach"
    DRAIN = "drain"
    MOVE = "move"
    REBUILD = "rebuild"
    RESTART = "restart"
    RETIRE = "retire"
    RETRY_LOGIN = "retry_login"
    SWAP = "swap"

    def __str__(self) -> str:
        return str(self.value)
