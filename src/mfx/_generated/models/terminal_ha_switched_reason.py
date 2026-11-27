from enum import Enum


class TerminalHaSwitchedReason(str, Enum):
    BROKER_LOST = "broker_lost"
    OPERATOR = "operator"
    ORDER = "order"
    PROCESS_GONE = "process_gone"
    TERMINAL_FAILED = "terminal_failed"
    UNRESPONSIVE = "unresponsive"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "TerminalHaSwitchedReason":
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
