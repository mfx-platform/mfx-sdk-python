from enum import Enum


class RiskPlanStepSpecHeldBy(str, Enum):
    BROKER = "broker"
    MFX = "mfx"

    def __str__(self) -> str:
        return str(self.value)
