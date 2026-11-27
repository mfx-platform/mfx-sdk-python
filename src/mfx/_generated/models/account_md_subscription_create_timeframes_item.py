from enum import Enum


class AccountMdSubscriptionCreateTimeframesItem(str, Enum):
    D1 = "D1"
    H1 = "H1"
    H4 = "H4"
    M1 = "M1"
    M15 = "M15"
    M30 = "M30"
    M5 = "M5"
    MN1 = "MN1"
    W1 = "W1"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "AccountMdSubscriptionCreateTimeframesItem":
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
