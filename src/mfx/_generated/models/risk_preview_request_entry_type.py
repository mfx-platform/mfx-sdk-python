from enum import Enum


class RiskPreviewRequestEntryType(str, Enum):
    LIMIT = "limit"
    MARKET = "market"
    STOP = "stop"

    def __str__(self) -> str:
        return str(self.value)
