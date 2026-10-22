from enum import Enum


class TerminalOperationKind(str, Enum):
    ATTACH = "attach"
    DETACH = "detach"
    DRAIN = "drain"
    MOVE = "move"
    REBUILD = "rebuild"
    RESTART = "restart"
    RETIRE = "retire"
    RETRY_LOGIN = "retry_login"

    def __str__(self) -> str:
        return str(self.value)
