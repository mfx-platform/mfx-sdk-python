from enum import Enum


class EaTrialState(str, Enum):
    ENDED = "ended"
    RUNNING = "running"

    def __str__(self) -> str:
        return str(self.value)
