from enum import Enum


class RiskPreviewVerdict(str, Enum):
    ALLOW = "allow"
    REFUSE = "refuse"

    def __str__(self) -> str:
        return str(self.value)
