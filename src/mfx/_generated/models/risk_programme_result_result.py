from enum import Enum


class RiskProgrammeResultResult(str, Enum):
    ENDED = "ended"
    FAILED = "failed"
    PASSED = "passed"

    def __str__(self) -> str:
        return str(self.value)
