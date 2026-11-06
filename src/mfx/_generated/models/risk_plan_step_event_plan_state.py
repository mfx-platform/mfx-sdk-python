from enum import Enum


class RiskPlanStepEventPlanState(str, Enum):
    ARMED = "armed"
    COMPLETED = "completed"
    DRAFT = "draft"
    ENDED = "ended"
    FAILED = "failed"
    MANAGING = "managing"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
