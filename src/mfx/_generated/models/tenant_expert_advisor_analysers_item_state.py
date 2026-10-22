from enum import Enum


class TenantExpertAdvisorAnalysersItemState(str, Enum):
    DONE = "done"
    FAILED = "failed"
    PENDING = "pending"
    RUNNING = "running"
    SKIPPED = "skipped"

    def __str__(self) -> str:
        return str(self.value)
