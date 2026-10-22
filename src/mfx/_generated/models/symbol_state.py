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
