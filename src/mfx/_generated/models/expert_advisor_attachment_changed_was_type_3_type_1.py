from enum import Enum


class ExpertAdvisorAttachmentChangedWasType3Type1(str, Enum):
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    DEPLOYING = "deploying"
    RUNNING = "running"
    TRIAL = "trial"

    def __str__(self) -> str:
        return str(self.value)
