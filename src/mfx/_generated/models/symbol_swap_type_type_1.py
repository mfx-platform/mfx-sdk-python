from enum import Enum


class SymbolSwapTypeType1(str, Enum):
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

    @classmethod
    def _read(cls, value: str) -> "SymbolSwapTypeType1":
        """A word from a response: its member, or, for a word a later version of the API added,
        an UNKNOWN pseudo-member whose value is the word as sent."""
        try:
            return cls(value)
        except ValueError:
            if not isinstance(value, str):
                raise
        unknown = str.__new__(cls, value)
        unknown._name_ = "UNKNOWN"
        unknown._value_ = value
        return unknown
