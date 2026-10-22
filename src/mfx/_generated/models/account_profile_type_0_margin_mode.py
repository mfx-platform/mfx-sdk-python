from enum import Enum


class AccountProfileType0MarginMode(str, Enum):
    EXCHANGE = "exchange"
    HEDGING = "hedging"
    NETTING = "netting"

    def __str__(self) -> str:
        return str(self.value)
