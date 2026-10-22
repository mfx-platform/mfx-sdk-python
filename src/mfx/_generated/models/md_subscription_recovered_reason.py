from enum import Enum


class MdSubscriptionRecoveredReason(str, Enum):
    NO_TICKS_IN_SESSION = "no_ticks_in_session"
    REPORT_STALE = "report_stale"
    SUBSCRIPTION_REFUSED = "subscription_refused"
    SYMBOL_REMOVED = "symbol_removed"
    TERMINAL_DISCONNECTED = "terminal_disconnected"

    def __str__(self) -> str:
        return str(self.value)
