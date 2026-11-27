from enum import Enum


class CommandKind(str, Enum):
    ORDER_CANCEL = "order_cancel"
    ORDER_MODIFY = "order_modify"
    ORDER_PLACE = "order_place"
    POSITION_CLOSE = "position_close"
    POSITION_CLOSE_BY = "position_close_by"
    POSITION_CLOSE_PARTIAL = "position_close_partial"
    POSITION_MODIFY = "position_modify"
    RISK_SYNC = "risk_sync"
    TRAILING_STOP_CLEAR = "trailing_stop_clear"
    TRAILING_STOP_SET = "trailing_stop_set"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "CommandKind":
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
