from enum import Enum


class RiskCoverageChangedFrom(str, Enum):
    DEGRADED = "degraded"
    DISCONNECTED = "disconnected"
    HEALTHY = "healthy"
    UNKNOWN = "unknown"

    def __str__(self) -> str:
        return str(self.value)
