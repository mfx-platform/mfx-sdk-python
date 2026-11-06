from enum import Enum


class RiskPlanStepHeldBy(str, Enum):
    BROKER = "broker"
    MFX = "mfx"

    def __str__(self) -> str:
        return str(self.value)
