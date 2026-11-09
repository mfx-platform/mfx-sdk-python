from enum import Enum


class CopyRiskLimitsBasis(str, Enum):
    BALANCE = "balance"
    EQUITY = "equity"

    def __str__(self) -> str:
        return str(self.value)
