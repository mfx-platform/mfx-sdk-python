from enum import Enum


class SymbolSwapTypeType2Type1(str, Enum):
    CURRENCY_DEPOSIT = "currency_deposit"
    CURRENCY_MARGIN = "currency_margin"
    CURRENCY_SYMBOL = "currency_symbol"
    DISABLED = "disabled"
    INTEREST_CURRENT = "interest_current"
    INTEREST_OPEN = "interest_open"
    POINTS = "points"
    REOPEN_BID = "reopen_bid"
    REOPEN_CURRENT = "reopen_current"

    def __str__(self) -> str:
        return str(self.value)
