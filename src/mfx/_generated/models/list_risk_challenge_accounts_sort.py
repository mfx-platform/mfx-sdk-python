from enum import Enum


class ListRiskChallengeAccountsSort(str, Enum):
    DAILY_LOSS_USED = "daily_loss_used"
    DRAWDOWN = "drawdown"
    PERIOD_ENDS_AT = "period_ends_at"
    PROFIT = "profit"
    TRADING_DAYS = "trading_days"

    def __str__(self) -> str:
        return str(self.value)
