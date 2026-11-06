from enum import Enum


class RiskCoverageChangedKind(str, Enum):
    BROKER_HELD = "broker_held"
    MANAGED_ACTIONS = "managed_actions"
    MONITORING = "monitoring"
    PRE_TRADE = "pre_trade"

    def __str__(self) -> str:
        return str(self.value)
