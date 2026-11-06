from enum import Enum


class RiskPlanStepSpecActionPctOfType1(str, Enum):
    ORIGINAL = "original"
    REMAINING = "remaining"

    def __str__(self) -> str:
        return str(self.value)
