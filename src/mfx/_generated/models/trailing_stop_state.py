from enum import Enum


class TrailingStopState(str, Enum):
    ACTIVE = "active"
    ENDED = "ended"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
