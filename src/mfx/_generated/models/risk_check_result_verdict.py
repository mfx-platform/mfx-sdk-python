from enum import Enum


class RiskCheckResultVerdict(str, Enum):
    ALLOW = "allow"
    REFUSE = "refuse"

    def __str__(self) -> str:
        return str(self.value)
