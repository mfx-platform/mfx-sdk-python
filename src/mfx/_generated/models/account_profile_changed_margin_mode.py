from enum import Enum


class AccountProfileChangedMarginMode(str, Enum):
    EXCHANGE = "exchange"
    HEDGING = "hedging"
    NETTING = "netting"

    def __str__(self) -> str:
        return str(self.value)
