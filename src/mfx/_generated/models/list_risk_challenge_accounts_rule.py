from enum import Enum


class ListRiskChallengeAccountsRule(str, Enum):
    DAILY_LOSS = "daily_loss"
    MAX_DRAWDOWN = "max_drawdown"

    def __str__(self) -> str:
        return str(self.value)
