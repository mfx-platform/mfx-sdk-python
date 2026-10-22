from enum import Enum


class ExpertAdvisorAttachmentChangedState(str, Enum):
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    DEPLOYING = "deploying"
    DETACHED = "detached"
    RUNNING = "running"
    TRIAL = "trial"

    def __str__(self) -> str:
        return str(self.value)
