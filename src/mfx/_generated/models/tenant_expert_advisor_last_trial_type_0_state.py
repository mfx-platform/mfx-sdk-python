from enum import Enum


class TenantExpertAdvisorLastTrialType0State(str, Enum):
    AWAITING_CONFIRMATION = "awaiting_confirmation"
    DETACHED = "detached"
    RUNNING = "running"
    TRIAL = "trial"

    def __str__(self) -> str:
        return str(self.value)
