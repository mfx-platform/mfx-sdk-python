from enum import Enum


class RiskChallengeAccountState(str, Enum):
    ENDED = "ended"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"

    def __str__(self) -> str:
        return str(self.value)
