from enum import Enum


class RiskPlanStepActionPctOfType3Type1(str, Enum):
    ORIGINAL = "original"
    REMAINING = "remaining"

    def __str__(self) -> str:
        return str(self.value)
