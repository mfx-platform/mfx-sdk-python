from enum import Enum


class BulkActionKind(str, Enum):
    CELL_RELOGIN = "cell_relogin"
    RESTART = "restart"
    RETIRE = "retire"
    SWAP = "swap"

    def __str__(self) -> str:
        return str(self.value)
