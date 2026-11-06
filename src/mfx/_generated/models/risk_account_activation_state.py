from enum import Enum


class RiskAccountActivationState(str, Enum):
    ACTIVE = "active"
    NONE = "none"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)
