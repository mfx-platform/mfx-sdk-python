from enum import Enum


class RiskActivityItemsItemOutcome(str, Enum):
    FAILED = "failed"
    PENDING = "pending"
    SKIPPED = "skipped"
    SUCCEEDED = "succeeded"
    UNRESOLVED = "unresolved"

    def __str__(self) -> str:
        return str(self.value)
