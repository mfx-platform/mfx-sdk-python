from enum import Enum


class CopyFollowerState(str, Enum):
    COPYING = "copying"
    PAUSED = "paused"
    STOPPED_OUT = "stopped_out"
    UNFOLLOWED = "unfollowed"

    def __str__(self) -> str:
        return str(self.value)
