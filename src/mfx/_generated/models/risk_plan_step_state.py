from enum import Enum


class RiskPlanStepState(str, Enum):
    ARMED = "armed"
    DONE = "done"
    FAILED = "failed"
    PARTLY = "partly"
    SKIPPED = "skipped"
    UNRESOLVED = "unresolved"
    WAITING = "waiting"

    def __str__(self) -> str:
        return str(self.value)
