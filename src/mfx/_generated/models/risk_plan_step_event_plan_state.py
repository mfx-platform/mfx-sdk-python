from enum import Enum


class RiskPlanStepEventPlanState(str, Enum):
    ARMED = "armed"
    COMPLETED = "completed"
    DRAFT = "draft"
    ENDED = "ended"
    FAILED = "failed"
    MANAGING = "managing"
    PAUSED = "paused"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "RiskPlanStepEventPlanState":
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
