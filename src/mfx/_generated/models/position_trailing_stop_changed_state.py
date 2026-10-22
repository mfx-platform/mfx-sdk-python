from enum import Enum


class PositionTrailingStopChangedState(str, Enum):
    ACTIVE = "active"
    ENDED = "ended"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
