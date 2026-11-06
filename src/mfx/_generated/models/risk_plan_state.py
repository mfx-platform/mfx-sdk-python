from enum import Enum


class RiskPlanState(str, Enum):
    ARMED = "armed"
    COMPLETED = "completed"
    DRAFT = "draft"
    ENDED = "ended"
    FAILED = "failed"
    MANAGING = "managing"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
