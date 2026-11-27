from enum import Enum


class SymbolState(str, Enum):
    CLOSED_SESSION = "closed_session"
    CLOSE_ONLY = "close_only"
    LONG_ONLY = "long_only"
    OPEN = "open"
    PAUSED = "paused"
    SHORT_ONLY = "short_only"
    TRADE_DISABLED = "trade_disabled"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "SymbolState":
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
