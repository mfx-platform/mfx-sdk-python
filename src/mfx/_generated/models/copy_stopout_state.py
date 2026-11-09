from enum import Enum


class CopyStopoutState(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    RESET = "reset"

    def __str__(self) -> str:
        return str(self.value)
