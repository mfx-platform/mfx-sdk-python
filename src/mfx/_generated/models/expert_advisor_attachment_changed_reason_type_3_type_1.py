from enum import Enum


class ExpertAdvisorAttachmentChangedReasonType3Type1(str, Enum):
    ATTACH_FAILED = "attach_failed"
    CONFIRMATION_EXPIRED = "confirmation_expired"
    REVOKED = "revoked"
    TERMINAL_RETIRED = "terminal_retired"
    TRIAL_FAILED = "trial_failed"

    def __str__(self) -> str:
        return str(self.value)
