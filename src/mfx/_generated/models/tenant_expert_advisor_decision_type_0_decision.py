from enum import Enum


class TenantExpertAdvisorDecisionType0Decision(str, Enum):
    APPROVE = "approve"
    ASK_CHANGE = "ask_change"
    REJECT = "reject"
    REVOKE = "revoke"

    def __str__(self) -> str:
        return str(self.value)
