from enum import Enum


class RiskBudgetKind(str, Enum):
    AMOUNT = "amount"
    PCT_OF_BALANCE = "pct_of_balance"
    PCT_OF_EQUITY = "pct_of_equity"

    def __str__(self) -> str:
        return str(self.value)
