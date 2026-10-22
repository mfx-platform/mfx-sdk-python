from enum import Enum


class TenantExpertAdvisorState(str, Enum):
    ANALYSING = "analysing"
    APPROVED = "approved"
    HELD = "held"
    JUDGED = "judged"
    REJECTED = "rejected"
    REVOKED = "revoked"
    UPLOADED = "uploaded"
    WITHDRAWN = "withdrawn"

    def __str__(self) -> str:
        return str(self.value)
