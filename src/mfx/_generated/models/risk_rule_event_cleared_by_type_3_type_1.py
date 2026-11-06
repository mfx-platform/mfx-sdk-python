from enum import Enum


class RiskRuleEventClearedByType3Type1(str, Enum):
    BELOW_WARN = "below_warn"
    OVERRIDE = "override"
    RESET = "reset"

    def __str__(self) -> str:
        return str(self.value)
