from enum import Enum


class RiskActionCompletedKind(str, Enum):
    BLOCK_ENTRIES = "block_entries"
    CANCEL_PENDING = "cancel_pending"
    CLOSE_PART = "close_part"
    CLOSE_POSITIONS = "close_positions"
    MOVE_STOP = "move_stop"
    SET_STOPS = "set_stops"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "RiskActionCompletedKind":
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
