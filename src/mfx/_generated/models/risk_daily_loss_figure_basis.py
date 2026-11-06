from enum import Enum


class RiskDailyLossFigureBasis(str, Enum):
    HIGHER_OF_BOTH = "higher_of_both"
    START_BALANCE = "start_balance"
    START_EQUITY = "start_equity"

    def __str__(self) -> str:
        return str(self.value)
