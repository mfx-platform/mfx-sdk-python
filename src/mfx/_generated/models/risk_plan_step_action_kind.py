from enum import Enum


class RiskPlanStepActionKind(str, Enum):
    CLOSE_PART = "close_part"
    MOVE_STOP = "move_stop"
    SET_STOPS = "set_stops"
    TRAIL = "trail"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "RiskPlanStepActionKind":
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
