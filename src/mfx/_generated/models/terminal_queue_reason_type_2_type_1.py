from enum import Enum


class TerminalQueueReasonType2Type1(str, Enum):
    BACKOFF = "backoff"
    BROKER_BUDGET = "broker_budget"
    BROKER_CAP = "broker_cap"
    BROKER_MAINTENANCE = "broker_maintenance"
    BULK_PACE = "bulk_pace"
    CELL_AT_STOP_LINE = "cell_at_stop_line"
    CELL_BUSY = "cell_busy"
    CELL_SETTLING = "cell_settling"
    CELL_SILENT = "cell_silent"
    PLATFORM_CEILING = "platform_ceiling"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "TerminalQueueReasonType2Type1":
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
