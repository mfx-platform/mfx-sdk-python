from enum import Enum


class TenantExpertAdvisorLastTrialType0EndedReasonType3Type1(str, Enum):
    CONFIRMATION_EXPIRED = "confirmation_expired"
    REVOKED = "revoked"
    TERMINAL_RETIRED = "terminal_retired"
    TRIAL_FAILED = "trial_failed"

    def __str__(self) -> str:
        return str(self.value)
