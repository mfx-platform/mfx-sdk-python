from enum import Enum


class CopyReason(str, Enum):
    ACCOUNT_NOT_CONNECTED = "account_not_connected"
    BROKER = "broker"
    CLOSE_ONLY = "close_only"
    MAPPING = "mapping"
    MARKET_CLOSED = "market_closed"
    MIN_VOLUME = "min_volume"
    NOT_ON_THIS_VENUE = "not_on_this_venue"
    NO_CONVERSION = "no_conversion"
    NO_STOP = "no_stop"
    PAUSED = "paused"
    PLAN_LIMIT = "plan_limit"
    RISK_RULE = "risk_rule"
    SIGNAL_EXPIRED = "signal_expired"
    SKIP_PENDING = "skip_pending"
    STOPPED_OUT = "stopped_out"
    VENUE_UNAVAILABLE = "venue_unavailable"

    def __str__(self) -> str:
        return str(self.value)
