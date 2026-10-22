from enum import Enum


class OwnContactRole(str, Enum):
    BILLING = "billing"
    REPRESENTATIVE = "representative"
    TECHNICAL = "technical"

    def __str__(self) -> str:
        return str(self.value)
