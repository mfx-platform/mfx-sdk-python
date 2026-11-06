from enum import Enum


class RiskOutcome(str, Enum):
    COMPLETED = "completed"
    DELIVERED = "delivered"
    FAILED = "failed"
    PARTLY = "partly"
    RECORDED = "recorded"
    RUNNING = "running"
    UNRESOLVED = "unresolved"

    def __str__(self) -> str:
        return str(self.value)
