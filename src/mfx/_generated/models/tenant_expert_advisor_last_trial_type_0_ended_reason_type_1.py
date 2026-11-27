from enum import Enum


class TenantExpertAdvisorLastTrialType0EndedReasonType1(str, Enum):
    CONFIRMATION_EXPIRED = "confirmation_expired"
    REVOKED = "revoked"
    TERMINAL_RETIRED = "terminal_retired"
    TRIAL_FAILED = "trial_failed"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "TenantExpertAdvisorLastTrialType0EndedReasonType1":
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
