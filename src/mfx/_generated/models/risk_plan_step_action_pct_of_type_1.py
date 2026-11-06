from enum import Enum


class RiskPlanStepActionPctOfType1(str, Enum):
    ORIGINAL = "original"
    REMAINING = "remaining"

    def __str__(self) -> str:
        return str(self.value)
