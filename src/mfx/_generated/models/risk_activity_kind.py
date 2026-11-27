from enum import Enum


class RiskActivityKind(str, Enum):
    ACTION = "action"
    BREACH = "breach"
    CHALLENGE_RESULT = "challenge_result"
    CLEAR = "clear"
    OUTSIDE_ENTRY = "outside_entry"
    OVERRIDE = "override"
    PLAN_CHANGE = "plan_change"
    POLICY_CHANGE = "policy_change"
    REFUSAL = "refusal"
    RESET = "reset"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def _read(cls, value: str) -> "RiskActivityKind":
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
