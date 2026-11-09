from enum import Enum


class CopyLeaderState(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    RETIRED = "retired"

    def __str__(self) -> str:
        return str(self.value)
