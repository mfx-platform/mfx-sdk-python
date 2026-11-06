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
