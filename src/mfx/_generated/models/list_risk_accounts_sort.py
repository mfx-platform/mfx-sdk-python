from enum import Enum


class ListRiskAccountsSort(str, Enum):
    DAILY_LOSS_USED = "daily_loss_used"
    DRAWDOWN_USED = "drawdown_used"
    EXPOSURE = "exposure"
    INPUTS_AGE = "inputs_age"

    def __str__(self) -> str:
        return str(self.value)
