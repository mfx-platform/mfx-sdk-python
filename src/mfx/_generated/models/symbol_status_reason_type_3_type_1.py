from enum import Enum


class SymbolStatusReasonType3Type1(str, Enum):
    NO_TICKS_IN_SESSION = "no_ticks_in_session"
    OUTSIDE_TRADE_SESSION = "outside_trade_session"
    REPORT_STALE = "report_stale"
    TERMINAL_DISCONNECTED = "terminal_disconnected"
    TRADE_MODE_CLOSE_ONLY = "trade_mode_close_only"
    TRADE_MODE_DISABLED = "trade_mode_disabled"
    TRADE_MODE_LONG_ONLY = "trade_mode_long_only"
    TRADE_MODE_SHORT_ONLY = "trade_mode_short_only"

    def __str__(self) -> str:
        return str(self.value)
