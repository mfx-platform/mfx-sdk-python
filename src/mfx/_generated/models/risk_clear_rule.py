from enum import Enum


class RiskClearRule(str, Enum):
    DAILY_LOSS = "daily_loss"
    DRAWDOWN = "drawdown"
    RESTRICTION = "restriction"

    def __str__(self) -> str:
        return str(self.value)
