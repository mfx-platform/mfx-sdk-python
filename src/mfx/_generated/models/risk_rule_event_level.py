from enum import Enum


class RiskRuleEventLevel(str, Enum):
    ACT = "act"
    CLEARED = "cleared"
    WARN = "warn"

    def __str__(self) -> str:
        return str(self.value)
