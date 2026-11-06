from enum import Enum


class RiskActionCompletedState(str, Enum):
    COMPLETED = "completed"
    FAILED = "failed"
    PARTLY = "partly"
    RUNNING = "running"
    UNRESOLVED = "unresolved"

    def __str__(self) -> str:
        return str(self.value)
