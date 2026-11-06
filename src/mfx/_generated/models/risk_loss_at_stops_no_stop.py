from enum import Enum


class RiskLossAtStopsNoStop(str, Enum):
    COUNT_NOTIONAL = "count_notional"
    REFUSE = "refuse"

    def __str__(self) -> str:
        return str(self.value)
