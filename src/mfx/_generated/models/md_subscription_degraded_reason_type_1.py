from enum import Enum


class MdSubscriptionDegradedReasonType1(str, Enum):
    BARS_GAP = "bars_gap"
    BARS_UNWATCHED = "bars_unwatched"
    NO_TICKS_IN_SESSION = "no_ticks_in_session"
    REPORT_STALE = "report_stale"
    SUBSCRIPTION_REFUSED = "subscription_refused"
    SYMBOL_REMOVED = "symbol_removed"
    TERMINAL_DISCONNECTED = "terminal_disconnected"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "MdSubscriptionDegradedReasonType1":
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
