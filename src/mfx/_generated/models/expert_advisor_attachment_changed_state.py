from enum import Enum


class ExpertAdvisorAttachmentChangedState(str, Enum):
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    DEPLOYING = "deploying"
    DETACHED = "detached"
    RUNNING = "running"
    TRIAL = "trial"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "ExpertAdvisorAttachmentChangedState":
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
